# Django Tastypie

Tastypie是一个web服务api框架,他提供了便捷,强大接口,高度抽象化.

Tastypie可以是models完全开放,但是你可以完全控制你想要开放的东西.

功能特性

- 支持:GET/POST/PUT/DELETE/PATCH
- 合理的配置
- 易扩展
- 包含多种序列化格式(JSON/XML/YAML/bplist)

开始

- 安装 pip install django-tastypie
- 添加到apps中:INSTALLED_APPS += ['tastypie']
- syncdb:./manage.py sysncdb
- 创建资源
- 将资源绑定到urlconf上

配置

唯一强制需要的配置是在INSTALLED_APPS中添加`tastypie`,tastypie的拥有正常的默认配置,并且不是必须的,除非你需要需改他们.详见(tastypie配置)

## 文档
`curl http://localhost:8000/api/v1/ `获取资源简要信息`http://localhost:8000/api/v1/?fullschema=true`获取所有信息

Resources.dispatch_list,调用dispatch
Resources.dispatch,取出Meta中配置的lists_allowed_methods,检查HTTP_X_HTTP_METHOD_OVERRIDE是否改写,request.method检查是否可处理,查找对应的处理方法,如果没有找到就报错,检查是否`is_authenticated`,检查`throttle_check`,调用method,调用`throttle`
Resource.post_list,先deserialize,在alter_deserialized_detail_data,再build_bundle,再obj_create,再get_resource_uri

## api请求过程

所有的 api 继承自 Resource,当请求到来时
1. 首先调用 `callback = getattr(self, view)` 通过 view 来获取对应的方法(dispatch_list,dispatch_detial,get_schema,get_multiple)
    1. 调用dispatch_list
        1.
```python
from __future__ import unicode_literals

from copy import deepcopy
from datetime import datetime
import logging
import sys
from time import mktime
import traceback
import warnings
from wsgiref.handlers import format_date_time

import django
from django.conf import settings
from django.conf.urls import url
from django.core.exceptions import (
    ObjectDoesNotExist, MultipleObjectsReturned, ValidationError,
)
from django.core.urlresolvers import (
    NoReverseMatch, reverse, Resolver404, get_script_prefix
)
from django.core.signals import got_request_exception
from django.core.exceptions import ImproperlyConfigured
try:
    from django.contrib.gis.db.models.fields import GeometryField
except (ImproperlyConfigured, ImportError):
    GeometryField = None
from django.db.models.constants import LOOKUP_SEP
try:
    from django.db.models.fields.related import\
        SingleRelatedObjectDescriptor as ReverseOneToOneDescriptor
except ImportError:
    from django.db.models.fields.related_descriptors import\
        ReverseOneToOneDescriptor
from django.db.models.sql.constants import QUERY_TERMS
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.utils import six
from django.utils.cache import patch_cache_control, patch_vary_headers
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt

from tastypie.authentication import Authentication
from tastypie.authorization import ReadOnlyAuthorization
from tastypie.bundle import Bundle
from tastypie.cache import NoCache
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie.exceptions import (
    NotFound, BadRequest, InvalidFilterError, HydrationError, InvalidSortError,
    ImmediateHttpResponse, Unauthorized, UnsupportedFormat,
)
from tastypie import fields
from tastypie import http
from tastypie.paginator import Paginator
from tastypie.serializers import Serializer
from tastypie.throttle import BaseThrottle
from tastypie.utils import (
    dict_strip_unicode_keys, is_valid_jsonp_callback_value, string_to_python,
    trailing_slash,
)
from tastypie.utils.mime import determine_format, build_content_type
from tastypie.validation import Validation
from tastypie.compat import get_module_name, atomic_decorator


def sanitize(text):
    # We put the single quotes back, due to their frequent usage in exception
    # messages.
    return escape(text).replace('&#39;', "'").replace('&quot;', '"')


class ResourceOptions(object):
    """
    A configuration class for ``Resource``.

    Provides sane defaults and the logic needed to augment these settings with
    the internal ``class Meta`` used on ``Resource`` subclasses.
    """
    serializer = Serializer()
    authentication = Authentication()
    authorization = ReadOnlyAuthorization()
    cache = NoCache()
    throttle = BaseThrottle()
    validation = Validation()
    paginator_class = Paginator
    allowed_methods = ['get', 'post', 'put', 'delete', 'patch']
    list_allowed_methods = None
    detail_allowed_methods = None
    limit = getattr(settings, 'API_LIMIT_PER_PAGE', 20)
    max_limit = 1000
    api_name = None
    resource_name = None
    urlconf_namespace = None
    default_format = 'application/json'
    filtering = {}
    ordering = []
    object_class = None
    queryset = None
    fields = []
    excludes = []
    include_resource_uri = True
    include_absolute_url = False
    always_return_data = False
    collection_name = 'objects'
    detail_uri_name = 'pk'

    def __new__(cls, meta=None):
        overrides = {}

        # Handle overrides.
        if meta:
            for override_name in dir(meta):
                # No internals please.
                if not override_name.startswith('_'):
                    overrides[override_name] = getattr(meta, override_name)

        allowed_methods = overrides.get('allowed_methods', ['get', 'post', 'put', 'delete', 'patch'])

        if overrides.get('list_allowed_methods', None) is None:
            overrides['list_allowed_methods'] = allowed_methods

        if overrides.get('detail_allowed_methods', None) is None:
            overrides['detail_allowed_methods'] = allowed_methods

        if six.PY3:
            return object.__new__(type('ResourceOptions', (cls,), overrides))
        else:
            return object.__new__(type(b'ResourceOptions', (cls,), overrides))


class DeclarativeMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['base_fields'] = {}
        declared_fields = {}

        # Inherit any fields from parent(s).
        parents = [b for b in bases if issubclass(b, Resource)]
        # Simulate the MRO.
        parents.reverse()
        for p in parents:
            parent_fields = getattr(p, 'base_fields', {})

            for field_name, field_object in parent_fields.items():
                attrs['base_fields'][field_name] = deepcopy(field_object)

        for field_name, obj in attrs.copy().items():
            # Look for ``dehydrated_type`` instead of doing ``isinstance``,
            # which can break down if Tastypie is re-namespaced as something
            # else.
            if hasattr(obj, 'dehydrated_type'):
                field = attrs.pop(field_name)
                declared_fields[field_name] = field

        attrs['base_fields'].update(declared_fields)
        attrs['declared_fields'] = declared_fields
        new_class = super(DeclarativeMetaclass, cls).__new__(cls, name, bases, attrs)
        opts = getattr(new_class, 'Meta', None)
        new_class._meta = ResourceOptions(opts)

        if not getattr(new_class._meta, 'resource_name', None):
            # No ``resource_name`` provided. Attempt to auto-name the resource.
            class_name = new_class.__name__
            name_bits = [bit for bit in class_name.split('Resource') if bit]
            resource_name = ''.join(name_bits).lower()
            new_class._meta.resource_name = resource_name

        if getattr(new_class._meta, 'include_resource_uri', True):
            if 'resource_uri' not in new_class.base_fields:
                new_class.base_fields['resource_uri'] = fields.CharField(readonly=True, verbose_name="resource uri")
        elif 'resource_uri' in new_class.base_fields and 'resource_uri' not in attrs:
            del(new_class.base_fields['resource_uri'])

        for field_name, field_object in new_class.base_fields.items():
            if hasattr(field_object, 'contribute_to_class'):
                field_object.contribute_to_class(new_class, field_name)

        return new_class


# print(six.with_metaclass(DeclarativeMetaclass).__new__.__code__.co_varnames)

class Resource(six.with_metaclass(DeclarativeMetaclass)):
    """
    Handles the data, request dispatch and responding to requests.

    Serialization/deserialization is handled "at the edges" (i.e. at the
    beginning/end of the request/response cycle) so that everything internally
    is Python data structures.

    This class tries to be non-model specific, so it can be hooked up to other
    data sources, such as search results, files, other data, etc.
    """
    def __init__(self, api_name=None):
        # this can cause:
        # TypeError: object.__new__(method-wrapper) is not safe, use method-wrapper.__new__()
        # when trying to copy a generator used as a default. Wrap call to
        # generator in lambda to get around this error.
        self.fields = deepcopy(self.base_fields)
        if api_name is not None:
            self._meta.api_name = api_name

    def __getattr__(self, name):
        try:
            return self.fields[name]
        except KeyError:
            raise AttributeError(name)

    def wrap_view(self, view):
        """
        Wraps methods so they can be called in a more functional way as well
        as handling exceptions better.

        Note that if ``BadRequest`` or an exception with a ``response`` attr
        are seen, there is special handling to either present a message back
        to the user or return the response traveling with the exception.
        """
        @csrf_exempt
        def wrapper(request, *args, **kwargs):
            try:
                # 第一步调用 ,根据 view 获取对应的方法,
                # 默认 args 为空, kwargs是{'api_name': 'v1', 'resource_name': 'project'}
                callback = getattr(self, view)
                response = callback(request, *args, **kwargs)

                # Our response can vary based on a number of factors, use
                # the cache class to determine what we should ``Vary`` on so
                # caches won't return the wrong (cached) version.
                varies = getattr(self._meta.cache, "varies", [])

                if varies:
                    patch_vary_headers(response, varies)

                if self._meta.cache.cacheable(request, response):
                    if self._meta.cache.cache_control():
                        # If the request is cacheable and we have a
                        # ``Cache-Control`` available then patch the header.
                        patch_cache_control(response, **self._meta.cache.cache_control())

                if request.is_ajax() and not response.has_header("Cache-Control"):
                    # IE excessively caches XMLHttpRequests, so we're disabling
                    # the browser cache here.
                    # See http://www.enhanceie.com/ie/bugs.asp for details.
                    patch_cache_control(response, no_cache=True)

                return response
            except (BadRequest, fields.ApiFieldError) as e:
                data = {"error": sanitize(e.args[0]) if getattr(e, 'args') else ''}
                return self.error_response(request, data, response_class=http.HttpBadRequest)
            except ValidationError as e:
                data = {"error": sanitize(e.messages)}
                return self.error_response(request, data, response_class=http.HttpBadRequest)
            except Exception as e:
                # Prevent muting non-django's exceptions
                # i.e. RequestException from 'requests' library
                if hasattr(e, 'response') and isinstance(e.response, HttpResponse):
                    return e.response

                # A real, non-expected exception.
                # Handle the case where the full traceback is more helpful
                # than the serialized error.
                if settings.DEBUG and getattr(settings, 'TASTYPIE_FULL_DEBUG', False):
                    raise

                # Re-raise the error to get a proper traceback when the error
                # happend during a test case
                if request.META.get('SERVER_NAME') == 'testserver':
                    raise

                # Rather than re-raising, we're going to things similar to
                # what Django does. The difference is returning a serialized
                # error message.
                return self._handle_500(request, e)

        return wrapper

    def _handle_500(self, request, exception):
        the_trace = '\n'.join(traceback.format_exception(*(sys.exc_info())))
        response_class = http.HttpApplicationError
        response_code = 500

        NOT_FOUND_EXCEPTIONS = (NotFound, ObjectDoesNotExist, Http404)

        if isinstance(exception, NOT_FOUND_EXCEPTIONS):
            response_class = HttpResponseNotFound
            response_code = 404

        elif isinstance(exception, UnsupportedFormat):
            response_class = http.HttpBadRequest
            response_code = 400

        if settings.DEBUG:
            data = {
                "error_message": sanitize(six.text_type(exception)),
                "traceback": the_trace,
            }
            return self.error_response(request, data, response_class=response_class)

        # When DEBUG is False, send an error message to the admins (unless it's
        # a 404, in which case we check the setting).

        if not response_code == 404:
            log = logging.getLogger('django.request.tastypie')
            log.error('Internal Server Error: %s' % request.path, exc_info=True,
                      extra={'status_code': response_code, 'request': request})

        # Send the signal so other apps are aware of the exception.
        got_request_exception.send(self.__class__, request=request)

        # Prep the data going out.
        data = {
            "error_message": getattr(settings, 'TASTYPIE_CANNED_ERROR', "Sorry, this request could not be processed. Please try again later."),
        }
        return self.error_response(request, data, response_class=response_class)

    def _build_reverse_url(self, name, args=None, kwargs=None):
        """
        A convenience hook for overriding how URLs are built.

        See ``NamespacedModelResource._build_reverse_url`` for an example.
        """
        return reverse(name, args=args, kwargs=kwargs)

    def base_urls(self):
        """
        The standard URLs this ``Resource`` should respond to.
        """
        return [
            url(r"^(?P<resource_name>%s)%s$" % (self._meta.resource_name, trailing_slash), self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema%s$" % (self._meta.resource_name, trailing_slash), self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/set/(?P<%s_list>.*?)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash), self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r"^(?P<resource_name>%s)/(?P<%s>.*?)%s$" % (self._meta.resource_name, self._meta.detail_uri_name, trailing_slash), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def override_urls(self):
        """
        Deprecated. Will be removed by v1.0.0. Please use ``prepend_urls`` instead.
        """
        return []

    def prepend_urls(self):
        """
        A hook for adding your own URLs or matching before the default URLs.
        """
        return []

    @property
    def urls(self):
        """
        The endpoints this ``Resource`` responds to.

        Mostly a standard URLconf, this is suitable for either automatic use
        when registered with an ``Api`` class or for including directly in
        a URLconf should you choose to.
        """
        urls = self.prepend_urls()

        overridden_urls = self.override_urls()
        if overridden_urls:
            warnings.warn("'override_urls' is a deprecated method & will be removed by v1.0.0. Please rename your method to ``prepend_urls``.")
            urls += overridden_urls

        urls += self.base_urls()
        return urls

    def determine_format(self, request):
        """
        Used to determine the desired format.

        Largely relies on ``tastypie.utils.mime.determine_format`` but here
        as a point of extension.
        """
        return determine_format(request, self._meta.serializer, default_format=self._meta.default_format)

    def serialize(self, request, data, format, options=None):
        """
        Given a request, data and a desired format, produces a serialized
        version suitable for transfer over the wire.

        Mostly a hook, this uses the ``Serializer`` from ``Resource._meta``.
        """
        options = options or {}

        if 'text/javascript' in format:
            # get JSONP callback name. default to "callback"
            callback = request.GET.get('callback', 'callback')

            if not is_valid_jsonp_callback_value(callback):
                raise BadRequest('JSONP callback name is invalid.')

            options['callback'] = callback

        return self._meta.serializer.serialize(data, format, options)

    def deserialize(self, request, data, format='application/json'):
        """
        Given a request, data and a format, deserializes the given data.

        It relies on the request properly sending a ``CONTENT_TYPE`` header,
        falling back to ``application/json`` if not provided.

        Mostly a hook, this uses the ``Serializer`` from ``Resource._meta``.
        """
        deserialized = self._meta.serializer.deserialize(data, format=request.META.get('CONTENT_TYPE', format))
        return deserialized

    def alter_list_data_to_serialize(self, request, data):
        """
        A hook to alter list data just before it gets serialized & sent to the user.

        Useful for restructuring/renaming aspects of the what's going to be
        sent.

        Should accommodate for a list of objects, generally also including
        meta data.
        """
        return data

    def alter_detail_data_to_serialize(self, request, data):
        """
        A hook to alter detail data just before it gets serialized & sent to the user.

        Useful for restructuring/renaming aspects of the what's going to be
        sent.

        Should accommodate for receiving a single bundle of data.
        """
        return data

    def alter_deserialized_list_data(self, request, data):
        """
        A hook to alter list data just after it has been received from the user &
        gets deserialized.

        Useful for altering the user data before any hydration is applied.
        """
        return data

    def alter_deserialized_detail_data(self, request, data):
        """
        A hook to alter detail data just after it has been received from the user &
        gets deserialized.

        Useful for altering the user data before any hydration is applied.
        """
        return data

    def dispatch_list(self, request, **kwargs):
        """
        A view for handling the various HTTP methods (GET/POST/PUT/DELETE) over
        the entire list of resources.

        Relies on ``Resource.dispatch`` for the heavy-lifting.
        """
        # 第二步调用 对于整个数据集合进行的操作,首先调用此方法,及当 url 是集合时,类似于 api/v1/company
        return self.dispatch('list', request, **kwargs)

    def dispatch_detail(self, request, **kwargs):
        """
        A view for handling the various HTTP methods (GET/POST/PUT/DELETE) on
        a single resource.

        Relies on ``Resource.dispatch`` for the heavy-lifting.
        """
        # 第二步调用 对于单个数据进行的操作,首先调用此方法,类似于 api/v1/company/1
        return self.dispatch('detail', request, **kwargs)


    def dispatch(self, request_type, request, **kwargs):
        """
        Handles the common operations (allowed HTTP method, authentication,
        throttling, method lookup) surrounding most CRUD interactions.
        """
        # 第三步调用
        # 获取在 _meta 中定义的允许调用的方法
        allowed_methods = getattr(self._meta, "%s_allowed_methods" % request_type, None)

        # 如果是浏览器进行的 api 请求,因为只支持, POST,GET 方法.所以使用HTTP_X_HTTP_METHOD_OVERRIDE来替换其他不能直接使用的方法
        if 'HTTP_X_HTTP_METHOD_OVERRIDE' in request.META:
            request.method = request.META['HTTP_X_HTTP_METHOD_OVERRIDE']

        # 这里就可以自定义请求方法名称例如 用户登录 ,可以设为HTTP_X_HTTP_METHOD_OVERRIDE = LOGIN,让后自定义 login_list 或者 login_detail 方法就可以

        # 检查当前请求的方法是否在允许 allowed_methods中, 如果请求方法是'options',或者方法不在allowed_methods中,
        # 则立即返回 HttpResponse(),返回的字符串是允许的方法列表
        # allows = ','.join([meth.upper() for meth in allowed])
        # response = http.HttpMethodNotAllowed(allows)
        # response['Allow'] = allows
        # raise ImmediateHttpResponse(response=response)
        request_method = self.method_check(request, allowed=allowed_methods)

        # 从当前对象中查找对应请求方法的函数
        method = getattr(self, "%s_%s" % (request_method, request_type), None)

        # 如果当前对象没有对应的请求方法,则返回错误
        if method is None:
            raise ImmediateHttpResponse(response=http.HttpNotImplemented())

        # 检查用户是否登录
        self.is_authenticated(request)

        # 检查用户的在制定时间内请求次数是否超过设置值,如果超过,则返回
        # response = http.HttpTooManyRequests()
        # if isinstance(throttle, int) and not isinstance(throttle, bool):
        #     response['Retry-After'] = throttle
        # elif isinstance(throttle, datetime):
        #     response['Retry-After'] = format_date_time(mktime(throttle.timetuple()))
        # raise ImmediateHttpResponse(response=response)
        self.throttle_check(request)

        # 上面检查完毕之后
        # All clear. Process the request.

        # 如果请求方法是 PUT,那么这里会调用request._load_post_and_files(),
        # 就是 修改 request的self._post, self._files
        # if self.content_type == 'multipart/form-data':
        #     if hasattr(self, '_body'):
        #         # Use already read data
        #         data = BytesIO(self._body)
        #     else:
        #         data = self
        #     try:
        #         self._post, self._files = self.parse_file_upload(self.META, data)
        #     except MultiPartParserError:
        #         # An error occurred while parsing POST data. Since when
        #         # formatting the error the request handler might access
        #         # self.POST, set self._post and self._file to prevent
        #         # attempts to parse POST data again.
        #         # Mark that an error occurred. This allows self.__repr__ to
        #         # be explicit about it instead of simply representing an
        #         # empty POST
        #         self._mark_post_parse_error()
        #         raise
        # elif self.content_type == 'application/x-www-form-urlencoded':
        #     self._post, self._files = QueryDict(self.body, encoding=self._encoding), MultiValueDict()
        # else:
        #     self._post, self._files = QueryDict(encoding=self._encoding), MultiValueDict()
        #
        #
        # def convert_post_to_VERB(request, verb):
        #     """
        #     Force Django to process the VERB.
        #     """
        #     if request.method == verb:#verb=="PUT"
        #         if hasattr(request, '_post'):
        #             del request._post
        #             del request._files
        #
        #         try:
        #             request.method = "POST"
        #             request._load_post_and_files()
        #             request.method = verb
        #         except AttributeError:
        #             request.META['REQUEST_METHOD'] = 'POST'
        #             request._load_post_and_files()
        #             request.META['REQUEST_METHOD'] = verb
        #         setattr(request, verb, request.POST)
        #
        #     return request
        #
        #
        # def convert_post_to_put(request):
        #     return convert_post_to_VERB(request, verb='PUT')
        request = convert_post_to_put(request)

        # 调用真正的处理方法
        # method get_list,post_list,put_list,patch_list,delete_list
        # get_detail,post_detail,put_detail,patch_detail,delete_detail
        # 默认post_detail返回 http.HttpNotImplemented()即501 NotImplemented
        response = method(request, **kwargs)

        # Add the throttled request.
        # 请求处理完成后,在这里增加一次请求记录
        self.log_throttled_access(request)

        # If what comes back isn't a ``HttpResponse``, assume that the
        # request was accepted and that some action occurred. This also
        # prevents Django from freaking out.
        # 如果处理方法处理结束后,没有返回HttpResponse, 则返回一个HttpNoContent()的 response
        if not isinstance(response, HttpResponse):
            return http.HttpNoContent()

        return response

    def remove_api_resource_names(self, url_dict):
        """
        Given a dictionary of regex matches from a URLconf, removes
        ``api_name`` and/or ``resource_name`` if found.

        This is useful for converting URLconf matches into something suitable
        for data lookup. For example::

            Model.objects.filter(**self.remove_api_resource_names(matches))
        """
        kwargs_subset = url_dict.copy()

        for key in ['api_name', 'resource_name']:
            try:
                del(kwargs_subset[key])
            except KeyError:
                pass

        return kwargs_subset

    def method_check(self, request, allowed=None):
        """
        Ensures that the HTTP method used on the request is allowed to be
        handled by the resource.

        Takes an ``allowed`` parameter, which should be a list of lowercase
        HTTP methods to check against. Usually, this looks like::

            # The most generic lookup.
            self.method_check(request, self._meta.allowed_methods)

            # A lookup against what's allowed for list-type methods.
            self.method_check(request, self._meta.list_allowed_methods)

            # A useful check when creating a new endpoint that only handles
            # GET.
            self.method_check(request, ['get'])
        """
        if allowed is None:
            allowed = []

        request_method = request.method.lower()
        allows = ','.join([meth.upper() for meth in allowed])

        if request_method == "options":
            response = HttpResponse(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        if request_method not in allowed:
            response = http.HttpMethodNotAllowed(allows)
            response['Allow'] = allows
            raise ImmediateHttpResponse(response=response)

        return request_method

    def is_authenticated(self, request):
        """
        Handles checking if the user is authenticated and dealing with
        unauthenticated users.

        Mostly a hook, this uses class assigned to ``authentication`` from
        ``Resource._meta``.
        """
        # Authenticate the request as needed.
        auth_result = self._meta.authentication.is_authenticated(request)

        if isinstance(auth_result, HttpResponse):
            raise ImmediateHttpResponse(response=auth_result)

        if auth_result is not True:
            raise ImmediateHttpResponse(response=http.HttpUnauthorized())

    def throttle_check(self, request):
        """
        Handles checking if the user should be throttled.

        Mostly a hook, this uses class assigned to ``throttle`` from
        ``Resource._meta``.
        """
        identifier = self._meta.authentication.get_identifier(request)

        # Check to see if they should be throttled.
        throttle = self._meta.throttle.should_be_throttled(identifier)

        if throttle:
            # Throttle limit exceeded.

            response = http.HttpTooManyRequests()

            if isinstance(throttle, int) and not isinstance(throttle, bool):
                response['Retry-After'] = throttle
            elif isinstance(throttle, datetime):
                response['Retry-After'] = format_date_time(mktime(throttle.timetuple()))

            raise ImmediateHttpResponse(response=response)

    def log_throttled_access(self, request):
        """
        Handles the recording of the user's access for throttling purposes.

        Mostly a hook, this uses class assigned to ``throttle`` from
        ``Resource._meta``.
        """
        request_method = request.method.lower()
        self._meta.throttle.accessed(self._meta.authentication.get_identifier(request), url=request.get_full_path(), request_method=request_method)

    def unauthorized_result(self, exception):
        raise ImmediateHttpResponse(response=http.HttpUnauthorized())

    def authorized_read_list(self, object_list, bundle):
        """
        Handles checking of permissions to see if the user has authorization
        to GET this resource.
        """
        try:
            auth_result = self._meta.authorization.read_list(object_list, bundle)
        except Unauthorized as e:
            self.unauthorized_result(e)

        return auth_result

    def authorized_read_detail(self, object_list, bundle):
        """
        Handles checking of permissions to see if the user has authorization
        to GET this resource.
        """
        try:
            auth_result = self._meta.authorization.read_detail(object_list, bundle)
            if auth_result is not True:
                raise Unauthorized()
        except Unauthorized as e:
            self.unauthorized_result(e)

        return auth_result

    def authorized_create_list(self, object_list, bundle):
        """
        Handles checking of permissions to see if the user has authorization
        to POST this resource.
        """
        try:
            auth_result = self._meta.authorization.create_list(object_list, bundle)
        except Unauthorized as e:
            self.unauthorized_result(e)

        return auth_result

    def authorized_create_detail(self, object_list, bundle):
        """
        Handles checking of permissions to see if the user has authorization
        to POST this resource.
        """
        try:
            auth_result = self._meta.authorization.create_detail(object_list, bundle)
            if auth_result is not True:
                raise Unauthorized()
        except Unauthorized as e:
            self.unauthorized_result(e)

        return auth_result

    def authorized_update_list(self, object_list, bundle):
        """
        Handles checking of permissions to see if the user has authorization
        to PUT this resource.
        """
        try:
            auth_result = self._meta.authorization.update_list(object_list, bundle)
        except Unauthorized as e:
            self.unauthorized_result(e)

        return auth_result

    def authorized_update_detail(self, object_list, bundle):
        """
        Handles checking of permissions to see if the user has authorization
        to PUT this resource.
        """
        try:
            auth_result = self._meta.authorization.update_detail(object_list, bundle)
            if auth_result is not True:
                raise Unauthorized()
        except Unauthorized as e:
            self.unauthorized_result(e)

        return auth_result

    def authorized_delete_list(self, object_list, bundle):
        """
        Handles checking of permissions to see if the user has authorization
        to DELETE this resource.
        """
        try:
            auth_result = self._meta.authorization.delete_list(object_list, bundle)
        except Unauthorized as e:
            self.unauthorized_result(e)

        return auth_result

    def authorized_delete_detail(self, object_list, bundle):
        """
        Handles checking of permissions to see if the user has authorization
        to DELETE this resource.
        """
        try:
            auth_result = self._meta.authorization.delete_detail(object_list, bundle)
            if not auth_result:
                raise Unauthorized()
        except Unauthorized as e:
            self.unauthorized_result(e)

        return auth_result

    def build_bundle(self, obj=None, data=None, request=None, objects_saved=None, via_uri=None):
        """
        Given either an object, a data dictionary or both, builds a ``Bundle``
        for use throughout the ``dehydrate/hydrate`` cycle.

        If no object is provided, an empty object from
        ``Resource._meta.object_class`` is created so that attempts to access
        ``bundle.obj`` do not fail.
        """
        if obj is None and self._meta.object_class:
            obj = self._meta.object_class()

        return Bundle(
            obj=obj,
            data=data,
            request=request,
            objects_saved=objects_saved,
            via_uri=via_uri
        )
    # 子类中具体构建过滤规则
    def build_filters(self, filters=None, ignore_bad_filters=False):
        """
        Allows for the filtering of applicable objects.

        This needs to be implemented at the user level.'

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        return filters

    def apply_sorting(self, obj_list, options=None):
        """
        Allows for the sorting of objects being returned.

        This needs to be implemented at the user level.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        return obj_list

    def get_bundle_detail_data(self, bundle):
        """
        Convenience method to return the ``detail_uri_name`` attribute off
        ``bundle.obj``.

        Usually just accesses ``bundle.obj.pk`` by default.
        """
        return getattr(bundle.obj, self._meta.detail_uri_name, None)

    # URL-related methods.

    def detail_uri_kwargs(self, bundle_or_obj):
        """
        Given a ``Bundle`` or an object (typically a ``Model`` instance),
        it returns the extra kwargs needed to generate a detail URI.

        By default, it uses this resource's ``detail_uri_name`` in order to
        create the URI.
        """
        kwargs = {}

        if isinstance(bundle_or_obj, Bundle):
            bundle_or_obj = bundle_or_obj.obj

        kwargs[self._meta.detail_uri_name] = getattr(bundle_or_obj, self._meta.detail_uri_name)

        return kwargs

    def resource_uri_kwargs(self, bundle_or_obj=None):
        """
        Builds a dictionary of kwargs to help generate URIs.

        Automatically provides the ``Resource.Meta.resource_name`` (and
        optionally the ``Resource.Meta.api_name`` if populated by an ``Api``
        object).

        If the ``bundle_or_obj`` argument is provided, it calls
        ``Resource.detail_uri_kwargs`` for additional bits to create
        """
        kwargs = {
            'resource_name': self._meta.resource_name,
        }

        if self._meta.api_name is not None:
            kwargs['api_name'] = self._meta.api_name

        if bundle_or_obj is not None:
            kwargs.update(self.detail_uri_kwargs(bundle_or_obj))

        return kwargs

    def get_resource_uri(self, bundle_or_obj=None, url_name='api_dispatch_list'):
        """
        Handles generating a resource URI.

        If the ``bundle_or_obj`` argument is not provided, it builds the URI
        for the list endpoint.

        If the ``bundle_or_obj`` argument is provided, it builds the URI for
        the detail endpoint.

        Return the generated URI. If that URI can not be reversed (not found
        in the URLconf), it will return an empty string.
        """
        if bundle_or_obj is not None:
            url_name = 'api_dispatch_detail'

        try:
            return self._build_reverse_url(url_name, kwargs=self.resource_uri_kwargs(bundle_or_obj))
        except NoReverseMatch:
            return ''

    def get_via_uri(self, uri, request=None):
        """
        This pulls apart the salient bits of the URI and populates the
        resource via a ``obj_get``.

        Optionally accepts a ``request``.

        If you need custom behavior based on other portions of the URI,
        simply override this method.
        """
        prefix = get_script_prefix()
        chomped_uri = uri

        if prefix and chomped_uri.startswith(prefix):
            chomped_uri = chomped_uri[len(prefix) - 1:]

        # We mangle the path a bit further & run URL resolution against *only*
        # the current class. This ought to prevent bad URLs from resolving to
        # incorrect data.
        found_at = chomped_uri.rfind(self._meta.resource_name)
        if found_at == -1:
            raise NotFound("An incorrect URL was provided '%s' for the '%s' resource." % (uri, self.__class__.__name__))
        chomped_uri = chomped_uri[found_at:]
        try:
            for url_resolver in getattr(self, 'urls', []):
                result = url_resolver.resolve(chomped_uri)

                if result is not None:
                    view, args, kwargs = result
                    break
            else:
                raise Resolver404("URI not found in 'self.urls'.")
        except Resolver404:
            raise NotFound("The URL provided '%s' was not a link to a valid resource." % uri)

        bundle = self.build_bundle(request=request)
        return self.obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))

    # Data preparation.

    def full_dehydrate(self, bundle, for_list=False):
        """
        Given a bundle with an object instance, extract the information from it
        to populate the resource.
        """
        # 对数据对象进行处理,构建为 data 字典,例如:
        # {
        # company_id: "/api/v1/company/1/",
        # end_date: "2017-08-31",
        # financial_statement_template_id: {
        # accounting_standard_id: "/api/v1/accounting_standard/1/",
        # id: 1,
        # name: "执行新准则的非上市公司财务报表(2014年7月1日后）",
        # resource_uri: "/api/v1/financial_statement_template/1/"
        # },
        # group_id: "/api/v1/group/1/",
        # id: 1,
        # in_charge_id: "/api/v1/user/2/",
        # initiate_date: "2017-06-05T18:32:22.253770",
        # name: "project1",
        # resource_uri: "/api/v1/project/1/",
        # start_date: "2017-01-01",
        # status: "",
        # user_id: null,
        # user_ids: [ ]
        # },
        data = bundle.data
        # api_name="v1"
        api_name = self._meta.api_name

        # resource_name='project'
        resource_name = self._meta.resource_name

        # Dehydrate each field.
        # {'company_id': <tastypie.fields.ForeignKey at 0x10a07bef0>,
        #  'end_date': <tastypie.fields.DateField at 0x10a07be80>,
        #  'financial_statement_template_id': <tastypie.fields.ToOneField at 0x10a07bfd0>,
        #  'group_id': <tastypie.fields.ToOneField at 0x10a07bc50>,
        #  'id': <tastypie.fields.IntegerField at 0x10a083080>,
        #  'in_charge_id': <tastypie.fields.ToOneField at 0x10a07bcc0>,
        #  'initiate_date': <tastypie.fields.DateTimeField at 0x10a07bf60>,
        #  'name': <tastypie.fields.CharField at 0x10a07bbe0>,
        #  resource_uri 是默认字段
        #  'resource_uri': <tastypie.fields.CharField at 0x10a07bb70>,
        #  'start_date': <tastypie.fields.DateField at 0x10a07be10>,
        #  'status': <tastypie.fields.CharField at 0x10a0830f0>,
        #  'user_id': <tastypie.fields.ToOneField at 0x10a07bd30>,
        #  'user_ids': <tastypie.fields.ToManyField at 0x10a07bda0>}

        # 对于每个字段进行处理
        for field_name, field_object in self.fields.items():
            # If it's not for use in this mode, skip
            # use_in ....目前不知为何
            field_use_in = field_object.use_in
            if callable(field_use_in):
                if not field_use_in(bundle):
                    continue
            else:
                if field_use_in not in ['all', 'list' if for_list else 'detail']:
                    continue

            # A touch leaky but it makes URI resolution work.
            # 如果是关联字段,这里经 v1/project传递过去
            if field_object.dehydrated_type == 'related':
                field_object.api_name = api_name
                field_object.resource_name = resource_name
            #  data['group_id']=调用该字段类型的dehydrate方法.来返回值
            # 例如这里:
            # data['group_id']="/api/v1/group/1/",
            # group_id 是关联字段

            # def dehydrate(self, bundle, for_list=True): # 非关联字段的dehydrate
            #        """
            #        Takes data from the provided object and prepares it for the
            #        resource.
            #        """
            #        # 如果当前字段没有attribute则检查字段默认值
            #        if self.attribute is not None:
            #            current_object = bundle.obj
            #            # 获取当前数据对象
            #            # 这里self._attrs例如['start_date']
            #            for attr in self._attrs:
            #                previous_object = current_object
            #                # 读取当前数据对象的对应属性值
            #                current_object = getattr(current_object, attr, None)
            #                # 如果当前对象为空,则尝试获取字段默认值,如果没有默认值,则字段的 null 属性是否 True,True 返回 None, 否则报错
            #                if current_object is None:
            #                    if self.has_default():
            #                        current_object = self._default
            #                        # Fall out of the loop, given any further attempts at
            #                        # accesses will fail miserably.
            #                        break
            #                    elif self.null:
            #                        current_object = None
            #                        # Fall out of the loop, given any further attempts at
            #                        # accesses will fail miserably.
            #                        break
            #                    else:
            #                        raise ApiFieldError("The object '%r' has an empty attribute '%s' and doesn't allow a default or null value." % (previous_object, attr))
            #            # 如果当前数据对象是函数,则调用该函数
            #            # 例如当前对象的的该字段是一个函数,那么使用该函数的返回值
            #            if callable(current_object):
            #                current_object = current_object()
            #            # 转换数据
            #            return self.convert(current_object)
            #         # 如果字段有默认值返回默认值否则返回None,
            #        if self.has_default():
            #            return self.convert(self.default)
            #        else:
            #            return None
            #
            #  关联字段的 dehydrate
            #
            # def dehydrate(self, bundle, for_list=True):
            #     foreign_obj = None
            #
            #     if callable(self.attribute):
            #         previous_obj = bundle.obj
            #         foreign_obj = self.attribute(bundle)
            #     elif isinstance(self.attribute, six.string_types):
            #         foreign_obj = bundle.obj
            #
            #         for attr in self._attrs:
            #             previous_obj = foreign_obj
            #             try:
            #                 foreign_obj = getattr(foreign_obj, attr, None)
            #             except ObjectDoesNotExist:
            #                 foreign_obj = None
            #
            #     if not foreign_obj:
            #         if not self.null:
            #             if callable(self.attribute):
            #                 raise ApiFieldError("The related resource for resource %s could not be found." % (previous_obj))
            #             else:
            #                 raise ApiFieldError("The model '%r' has an empty attribute '%s' and doesn't allow a null value." % (previous_obj, attr))
            #         return None
            #
            #     fk_resource = self.get_related_resource(foreign_obj)
            #     fk_bundle = Bundle(obj=foreign_obj, request=bundle.request)
            #     # 构建关联对象
            #     return self.dehydrate_related(fk_bundle, fk_resource, for_list=for_list)
            data[field_name] = field_object.dehydrate(bundle, for_list=for_list)

            # Check for an optional method to do further dehydration.
            # 如过当前对象的资源类中包含 本字段的dehydrate_[start_date] 则调用
            method = getattr(self, "dehydrate_%s" % field_name, None)

            if method:
                data[field_name] = method(bundle)

        # 直接返回 bundle 如果想要对要返回的数据对象在更进一步处理,可以在dehydrate中处理
        bundle = self.dehydrate(bundle)
        return bundle

    def dehydrate(self, bundle):
        """
        A hook to allow a final manipulation of data once all fields/methods
        have built out the dehydrated data.

        Useful if you need to access more than one dehydrated field or want
        to annotate on additional data.

        Must return the modified bundle.
        """
        return bundle

    def full_hydrate(self, bundle):
        """
        Given a populated bundle, distill it and turn it back into
        a full-fledged object instance.
        """
        if bundle.obj is None:
            bundle.obj = self._meta.object_class()

        bundle = self.hydrate(bundle)

        for field_name, field_object in self.fields.items():
            if field_object.readonly is True:
                continue

            # Check for an optional method to do further hydration.
            method = getattr(self, "hydrate_%s" % field_name, None)

            if method:
                bundle = method(bundle)

            if field_object.attribute:
                value = field_object.hydrate(bundle)

                # NOTE: We only get back a bundle when it is related field.
                if isinstance(value, Bundle) and value.errors.get(field_name):
                    bundle.errors[field_name] = value.errors[field_name]

                if value is not None or field_object.null:
                    # We need to avoid populating M2M data here as that will
                    # cause things to blow up.
                    if not field_object.is_related:
                        setattr(bundle.obj, field_object.attribute, value)
                    elif not field_object.is_m2m:
                        if value is not None:
                            # NOTE: A bug fix in Django (ticket #18153) fixes incorrect behavior
                            # which Tastypie was relying on.  To fix this, we store value.obj to
                            # be saved later in save_related.
                            try:
                                setattr(bundle.obj, field_object.attribute, value.obj)
                            except (ValueError, ObjectDoesNotExist):
                                bundle.related_objects_to_save[field_object.attribute] = value.obj
                        elif field_object.null:
                            if not isinstance(getattr(bundle.obj.__class__, field_object.attribute, None), ReverseOneToOneDescriptor):
                                # only update if not a reverse one to one field
                                setattr(bundle.obj, field_object.attribute, value)
                        elif field_object.blank:
                            continue

        return bundle

    def hydrate(self, bundle):
        """
        A hook to allow an initial manipulation of data before all methods/fields
        have built out the hydrated data.

        Useful if you need to access more than one hydrated field or want
        to annotate on additional data.

        Must return the modified bundle.
        """
        return bundle

    def hydrate_m2m(self, bundle):
        """
        Populate the ManyToMany data on the instance.
        """
        if bundle.obj is None:
            raise HydrationError("You must call 'full_hydrate' before attempting to run 'hydrate_m2m' on %r." % self)

        for field_name, field_object in self.fields.items():
            if not field_object.is_m2m:
                continue

            if field_object.attribute:
                # Note that we only hydrate the data, leaving the instance
                # unmodified. It's up to the user's code to handle this.
                # The ``ModelResource`` provides a working baseline
                # in this regard.
                bundle.data[field_name] = field_object.hydrate_m2m(bundle)

        for field_name, field_object in self.fields.items():
            if not field_object.is_m2m:
                continue

            method = getattr(self, "hydrate_%s" % field_name, None)

            if method:
                method(bundle)

        return bundle

    def build_schema(self):
        """
        Returns a dictionary of all the fields on the resource and some
        properties about those fields.

        Used by the ``schema/`` endpoint to describe what will be available.
        """
        data = {
            'fields': {},
            'default_format': self._meta.default_format,
            'allowed_list_http_methods': self._meta.list_allowed_methods,
            'allowed_detail_http_methods': self._meta.detail_allowed_methods,
            'default_limit': self._meta.limit,
        }

        if self._meta.ordering:
            data['ordering'] = self._meta.ordering

        if self._meta.filtering:
            data['filtering'] = self._meta.filtering

        # Skip assigning pk_field_name for non-model resources
        try:
            pk_field_name = self._meta.queryset.model._meta.pk.name
        except AttributeError:
            pk_field_name = None

        for field_name, field_object in self.fields.items():
            data['fields'][field_name] = {
                'default': field_object.default,
                'type': field_object.dehydrated_type,
                'nullable': field_object.null,
                'blank': field_object.blank,
                'readonly': field_object.readonly,
                'help_text': field_object.help_text,
                'unique': field_object.unique,
                'primary_key': True if field_name == pk_field_name else False,
                'verbose_name': field_object.verbose_name or field_name.replace("_", " "),
            }

            if field_object.dehydrated_type == 'related':
                if field_object.is_m2m:
                    related_type = 'to_many'
                else:
                    related_type = 'to_one'
                data['fields'][field_name]['related_type'] = related_type
                try:
                    uri = reverse('api_get_schema', kwargs={
                        'api_name': self._meta.api_name,
                        'resource_name': field_object.to_class()._meta.resource_name
                    })
                except NoReverseMatch:
                    uri = ''
                data['fields'][field_name]['related_schema'] = uri

        return data

    def dehydrate_resource_uri(self, bundle):
        """
        For the automatically included ``resource_uri`` field, dehydrate
        the URI for the given bundle.

        Returns empty string if no URI can be generated.
        """
        try:
            return self.get_resource_uri(bundle)
        except NotImplementedError:
            return ''
        except NoReverseMatch:
            return ''

    def generate_cache_key(self, *args, **kwargs):
        """
        Creates a unique-enough cache key.

        This is based off the current api_name/resource_name/args/kwargs.
        """
        smooshed = ["%s=%s" % (key, value) for key, value in kwargs.items()]

        # Use a list plus a ``.join()`` because it's faster than concatenation.
        return "%s:%s:%s:%s" % (self._meta.api_name, self._meta.resource_name, ':'.join(args), ':'.join(sorted(smooshed)))

    # Data access methods.

    def get_object_list(self, request):
        """
        A hook to allow making returning the list of available objects.

        This needs to be implemented at the user level.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        raise NotImplementedError()

    def can_create(self):
        """
        Checks to ensure ``post`` is within ``allowed_methods``.
        """
        allowed = set(self._meta.list_allowed_methods + self._meta.detail_allowed_methods)
        return 'post' in allowed

    def can_update(self):
        """
        Checks to ensure ``put`` is within ``allowed_methods``.

        Used when hydrating related data.
        """
        allowed = set(self._meta.list_allowed_methods + self._meta.detail_allowed_methods)
        return 'put' in allowed

    def can_delete(self):
        """
        Checks to ensure ``delete`` is within ``allowed_methods``.
        """
        allowed = set(self._meta.list_allowed_methods + self._meta.detail_allowed_methods)
        return 'delete' in allowed

    def apply_filters(self, request, applicable_filters):
        """
        A hook to alter how the filters are applied to the object list.

        This needs to be implemented at the user level.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        raise NotImplementedError()

    def obj_get_list(self, bundle, **kwargs):
        """
        Fetches the list of objects available on the resource.

        This needs to be implemented at the user level.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        raise NotImplementedError()

    def cached_obj_get_list(self, bundle, **kwargs):
        """
        A version of ``obj_get_list`` that uses the cache as a means to get
        commonly-accessed data faster.
        """
        cache_key = self.generate_cache_key('list', **kwargs)
        obj_list = self._meta.cache.get(cache_key)

        if obj_list is None:
            obj_list = self.obj_get_list(bundle=bundle, **kwargs)
            self._meta.cache.set(cache_key, obj_list)

        return obj_list

    def obj_get(self, bundle, **kwargs):
        """
        Fetches an individual object on the resource.

        This needs to be implemented at the user level. If the object can not
        be found, this should raise a ``NotFound`` exception.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        raise NotImplementedError()

    def cached_obj_get(self, bundle, **kwargs):
        """
        A version of ``obj_get`` that uses the cache as a means to get
        commonly-accessed data faster.
        """
        cache_key = self.generate_cache_key('detail', **kwargs)
        cached_bundle = self._meta.cache.get(cache_key)

        if cached_bundle is None:
            cached_bundle = self.obj_get(bundle=bundle, **kwargs)
            self._meta.cache.set(cache_key, cached_bundle)

        return cached_bundle

    def obj_create(self, bundle, **kwargs):
        """
        Creates a new object based on the provided data.

        This needs to be implemented at the user level.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        raise NotImplementedError()

    def obj_update(self, bundle, **kwargs):
        """
        Updates an existing object (or creates a new object) based on the
        provided data.

        This needs to be implemented at the user level.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        raise NotImplementedError()

    def obj_delete_list(self, bundle, **kwargs):
        """
        Deletes an entire list of objects.

        This needs to be implemented at the user level.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        raise NotImplementedError()

    def obj_delete_list_for_update(self, bundle, **kwargs):
        """
        Deletes an entire list of objects, specific to PUT list.

        This needs to be implemented at the user level.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        raise NotImplementedError()

    def obj_delete(self, bundle, **kwargs):
        """
        Deletes a single object.

        This needs to be implemented at the user level.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        raise NotImplementedError()

    def create_response(self, request, data, response_class=HttpResponse, **response_kwargs):
        """
        Extracts the common "which-format/serialize/return-response" cycle.

        Mostly a useful shortcut/hook.
        """
        desired_format = self.determine_format(request)
        serialized = self.serialize(request, data, desired_format)
        return response_class(content=serialized, content_type=build_content_type(desired_format), **response_kwargs)

    def error_response(self, request, errors, response_class=None):
        """
        Extracts the common "which-format/serialize/return-error-response"
        cycle.

        Should be used as much as possible to return errors.
        """
        if response_class is None:
            response_class = http.HttpBadRequest

        desired_format = None

        if request:
            if request.GET.get('callback', None) is None:
                try:
                    desired_format = self.determine_format(request)
                except BadRequest:
                    pass  # Fall through to default handler below
            else:
                # JSONP can cause extra breakage.
                desired_format = 'application/json'

        if not desired_format:
            desired_format = self._meta.default_format

        try:
            serialized = self.serialize(request, errors, desired_format)
        except BadRequest as e:
            error = "Additional errors occurred, but serialization of those errors failed."

            if settings.DEBUG:
                error += " %s" % e

            return response_class(content=error, content_type='text/plain')

        return response_class(content=serialized, content_type=build_content_type(desired_format))

    def is_valid(self, bundle):
        """
        Handles checking if the data provided by the user is valid.

        Mostly a hook, this uses class assigned to ``validation`` from
        ``Resource._meta``.

        If validation fails, an error is raised with the error messages
        serialized inside it.
        """
        errors = self._meta.validation.is_valid(bundle, bundle.request)

        if errors:
            bundle.errors[self._meta.resource_name] = errors
            return False

        return True

    def rollback(self, bundles):
        """
        Given the list of bundles, delete all objects pertaining to those
        bundles.

        This needs to be implemented at the user level. No exceptions should
        be raised if possible.

        ``ModelResource`` includes a full working version specific to Django's
        ``Models``.
        """
        raise NotImplementedError()

    # Views.
    # 获取对象集合
    def get_list(self, request, **kwargs):
        """
        Returns a serialized list of resources.

        Calls ``obj_get_list`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        # TODO: Uncached for now. Invalidation that works for everyone may be
        #       impossible.
        #
        # def build_bundle(self, obj=None, data=None, request=None, objects_saved=None, via_uri=None):
        #     """
        #     Given either an object, a data dictionary or both, builds a ``Bundle``
        #     for use throughout the ``dehydrate/hydrate`` cycle.
        #
        #     If no object is provided, an empty object from
        #     ``Resource._meta.object_class`` is created so that attempts to access
        #     ``bundle.obj`` do not fail.
        #     """
        #     if obj is None and self._meta.object_class:
        #         obj = self._meta.object_class()
        #     obj 是数据对象
        #     return Bundle(
        #         obj=obj,
        #         data=data,
        #         request=request,
        #         objects_saved=objects_saved,
        #         via_uri=via_uri
        #     )
        # 这里是获取数据集合,所以不存在 obj,data
        # base_bundle={
        # self.obj = self._meta.object_class()
        # self.data = {}
        # self.request = request
        # self.related_obj = None
        # self.related_name = None
        # self.errors = {}
        # self.objects_saved = set()
        # self.related_objects_to_save = {}
        # self.via_uri = None
        # }
        base_bundle = self.build_bundle(request=request)

        # 子类必须重写obj_get_list
        # kwargs:{'api_name': 'v1', 'resource_name': 'project'}
        # self.remove_api_resource_names(kwargs)
        # 这里会把 'api_name', 'resource_name'键删除掉
        # 最后返回 {}
        # def remove_api_resource_names(self, url_dict):
        #     """
        #     Given a dictionary of regex matches from a URLconf, removes
        #     ``api_name`` and/or ``resource_name`` if found.
        #
        #     This is useful for converting URLconf matches into something suitable
        #     for data lookup. For example::
        #
        #         Model.objects.filter(**self.remove_api_resource_names(matches))
        #     """
        #     kwargs_subset = url_dict.copy()
        #
        #     for key in ['api_name', 'resource_name']:
        #         try:
        #             del(kwargs_subset[key])
        #         except KeyError:
        #             pass
        #     return kwargs_subset


        # def obj_get_list(self, bundle, **kwargs):
        #     """
        #     A ORM-specific implementation of ``obj_get_list``.
        #
        #     ``GET`` dictionary of bundle.request can be used to narrow the query.
        #     """
        #     filters = {}
        #
        #     if hasattr(bundle.request, 'GET'):
        #         # Grab a mutable copy.
        #         filters = bundle.request.GET.copy()
        #
        #     # Update with the provided kwargs.
        #     filters.update(kwargs)
        #     # 取出 GET 参数
        #     # 构建 过滤规则
        #     applicable_filters = self.build_filters(filters=filters)
        #
        #     try:
        #        # 使用过滤规则进行过滤
        #         objects = self.apply_filters(bundle.request, applicable_filters)
        #        # ModelResource这里直接调用 queryset.filter(applicable_filters)
        #         return self.authorized_read_list(objects, bundle)
        #     except ValueError:
        #         raise BadRequest("Invalid resource lookup data provided (mismatched type).")


        # self.obj_get_list(bundle=base_bundle, **{})
        objects = self.obj_get_list(bundle=base_bundle, **self.remove_api_resource_names(kwargs))

        # 对取出来的数据集合进行排序
        # 这里会按照请求的 order_by或者 sort_by参数进行排序
        # http://localhost:8000/api/v1/project/?order_by=start_date&order_by=-end_date&limit=47
        # 这里会使用 query_set.order_by(**['start_date','-end_date'])
        sorted_objects = self.apply_sorting(objects, options=request.GET)

        # 对排序后的数据集合进行分页
        paginator = self._meta.paginator_class(request.GET, sorted_objects,resource_uri=self.get_resource_uri(),limit=self._meta.limit, max_limit=self._meta.max_limit, collection_name=self._meta.collection_name)

        # 取出对应页面数据,
        #  self._meta.collection_name 默认为' objects'

        # def page(self):
        #     """
        #     Generates all pertinent data about the requested page.
        #
        #     Handles getting the correct ``limit`` & ``offset``, then slices off
        #     the correct set of results and returns all pertinent metadata.
        #     """
        #     limit = self.get_limit()
        #     offset = self.get_offset()
        #     count = self.get_count()
        #     objects = self.get_slice(limit, offset)
        #     meta = {
        #         'offset': offset,
        #         'limit': limit,
        #         'total_count': count,
        #     }
        #
        #     if limit:
        #         meta['previous'] = self.get_previous(limit, offset)
        #         meta['next'] = self.get_next(limit, offset, count)
        #
        #     return {
        #         self.collection_name: objects,
        #         'meta': meta,
        #     }
        #
        #
        # 对于 django ORM 这里执行了get_slice(limit, offset)
        # def get_slice(self, limit, offset):
        #     """
        #     Slices the result set to the specified ``limit`` & ``offset``.
        #     """
        #     if limit == 0:
        #         return self.objects[offset:]
        #
        #     return self.objects[offset:offset + limit]

        to_be_serialized = paginator.page()

        # 到这里已经取出了需要的数据集合了

        # Dehydrate the bundles in preparation for serialization.
        # 对每一数据对象执行full_dehydrate
        # base_bundle={
        # self.obj = obj
        # self.data = {}
        # self.request = request
        # self.related_obj = None
        # self.related_name = None
        # self.errors = {}
        # self.objects_saved = set()
        # self.related_objects_to_save = {}
        # self.via_uri = None
        # }
        #
        bundles = [
            self.full_dehydrate(self.build_bundle(obj=obj, request=request), for_list=True)
            for obj in to_be_serialized[self._meta.collection_name]
        ]


        to_be_serialized[self._meta.collection_name] = bundles
        to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
        return self.create_response(request, to_be_serialized)

    def get_detail(self, request, **kwargs):
        """
        Returns a single serialized resource.

        Calls ``cached_obj_get/obj_get`` to provide the data, then handles that result
        set and serializes it.

        Should return a HttpResponse (200 OK).
        """
        basic_bundle = self.build_bundle(request=request)

        try:
            obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)
        return self.create_response(request, bundle)

    def post_list(self, request, **kwargs):
        """
        Creates a new resource/object with the provided data.

        Calls ``obj_create`` with the provided data and returns a response
        with the new resource's location.

        If a new resource is created, return ``HttpCreated`` (201 Created).
        If ``Meta.always_return_data = True``, there will be a populated body
        of serialized data.
        """
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)
        updated_bundle = self.obj_create(bundle, **self.remove_api_resource_names(kwargs))
        location = self.get_resource_uri(updated_bundle)

        if not self._meta.always_return_data:
            return http.HttpCreated(location=location)
        else:
            updated_bundle = self.full_dehydrate(updated_bundle)
            updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
            return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)

    def post_detail(self, request, **kwargs):
        """
        Creates a new subcollection of the resource under a resource.

        This is not implemented by default because most people's data models
        aren't self-referential.

        If a new resource is created, return ``HttpCreated`` (201 Created).
        """
        return http.HttpNotImplemented()

    def put_list(self, request, **kwargs):
        """
        Replaces a collection of resources with another collection.

        Calls ``delete_list`` to clear out the collection then ``obj_create``
        with the provided the data to create the new collection.

        Return ``HttpNoContent`` (204 No Content) if
        ``Meta.always_return_data = False`` (default).

        Return ``HttpAccepted`` (200 OK) if
        ``Meta.always_return_data = True``.
        """
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_list_data(request, deserialized)

        if self._meta.collection_name not in deserialized:
            raise BadRequest("Invalid data sent: missing '%s'" % self._meta.collection_name)

        basic_bundle = self.build_bundle(request=request)
        self.obj_delete_list_for_update(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        bundles_seen = []

        for object_data in deserialized[self._meta.collection_name]:
            bundle = self.build_bundle(data=dict_strip_unicode_keys(object_data), request=request)

            # Attempt to be transactional, deleting any previously created
            # objects if validation fails.
            try:
                self.obj_create(bundle=bundle, **self.remove_api_resource_names(kwargs))
                bundles_seen.append(bundle)
            except ImmediateHttpResponse:
                self.rollback(bundles_seen)
                raise

        if not self._meta.always_return_data:
            return http.HttpNoContent()
        else:
            to_be_serialized = {
                self._meta.collection_name: [
                    self.full_dehydrate(b, for_list=True)
                    for b in bundles_seen
                ]
            }
            to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
            return self.create_response(request, to_be_serialized)

    def put_detail(self, request, **kwargs):
        """
        Either updates an existing resource or creates a new one with the
        provided data.

        Calls ``obj_update`` with the provided data first, but falls back to
        ``obj_create`` if the object does not already exist.

        If a new resource is created, return ``HttpCreated`` (201 Created).
        If ``Meta.always_return_data = True``, there will be a populated body
        of serialized data.

        If an existing resource is modified and
        ``Meta.always_return_data = False`` (default), return ``HttpNoContent``
        (204 No Content).
        If an existing resource is modified and
        ``Meta.always_return_data = True``, return ``HttpAccepted`` (200
        OK).
        """
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        deserialized = self.alter_deserialized_detail_data(request, deserialized)
        bundle = self.build_bundle(data=dict_strip_unicode_keys(deserialized), request=request)

        try:
            updated_bundle = self.obj_update(bundle=bundle, **self.remove_api_resource_names(kwargs))

            if not self._meta.always_return_data:
                return http.HttpNoContent()
            else:
                # Invalidate prefetched_objects_cache for bundled object
                # because we might have changed a prefetched field
                updated_bundle.obj._prefetched_objects_cache = {}
                updated_bundle = self.full_dehydrate(updated_bundle)
                updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
                return self.create_response(request, updated_bundle)
        except (NotFound, MultipleObjectsReturned):
            updated_bundle = self.obj_create(bundle=bundle, **self.remove_api_resource_names(kwargs))
            location = self.get_resource_uri(updated_bundle)

            if not self._meta.always_return_data:
                return http.HttpCreated(location=location)
            else:
                updated_bundle = self.full_dehydrate(updated_bundle)
                updated_bundle = self.alter_detail_data_to_serialize(request, updated_bundle)
                return self.create_response(request, updated_bundle, response_class=http.HttpCreated, location=location)

    def delete_list(self, request, **kwargs):
        """
        Destroys a collection of resources/objects.

        Calls ``obj_delete_list``.

        If the resources are deleted, return ``HttpNoContent`` (204 No Content).
        """
        bundle = self.build_bundle(request=request)
        self.obj_delete_list(bundle=bundle, request=request, **self.remove_api_resource_names(kwargs))
        return http.HttpNoContent()

    def delete_detail(self, request, **kwargs):
        """
        Destroys a single resource/object.

        Calls ``obj_delete``.

        If the resource is deleted, return ``HttpNoContent`` (204 No Content).
        If the resource did not exist, return ``Http404`` (404 Not Found).
        """
        # Manually construct the bundle here, since we don't want to try to
        # delete an empty instance.
        bundle = Bundle(request=request)

        try:
            self.obj_delete(bundle=bundle, **self.remove_api_resource_names(kwargs))
            return http.HttpNoContent()
        except NotFound:
            return http.HttpNotFound()

    def patch_list(self, request, **kwargs):
        """
        Updates a collection in-place.

        The exact behavior of ``PATCH`` to a list resource is still the matter of
        some debate in REST circles, and the ``PATCH`` RFC isn't standard. So the
        behavior this method implements (described below) is something of a
        stab in the dark. It's mostly cribbed from GData, with a smattering
        of ActiveResource-isms and maybe even an original idea or two.

        The ``PATCH`` format is one that's similar to the response returned from
        a ``GET`` on a list resource::

            {
              "objects": [{object}, {object}, ...],
              "deleted_objects": ["URI", "URI", "URI", ...],
            }

        For each object in ``objects``:

            * If the dict does not have a ``resource_uri`` key then the item is
              considered "new" and is handled like a ``POST`` to the resource list.

            * If the dict has a ``resource_uri`` key and the ``resource_uri`` refers
              to an existing resource then the item is a update; it's treated
              like a ``PATCH`` to the corresponding resource detail.

            * If the dict has a ``resource_uri`` but the resource *doesn't* exist,
              then this is considered to be a create-via-``PUT``.

        Each entry in ``deleted_objects`` referes to a resource URI of an existing
        resource to be deleted; each is handled like a ``DELETE`` to the relevent
        resource.

        In any case:

            * If there's a resource URI it *must* refer to a resource of this
              type. It's an error to include a URI of a different resource.

            * ``PATCH`` is all or nothing. If a single sub-operation fails, the
              entire request will fail and all resources will be rolled back.

          * For ``PATCH`` to work, you **must** have ``put`` in your
            :ref:`detail-allowed-methods` setting.

          * To delete objects via ``deleted_objects`` in a ``PATCH`` request you
            **must** have ``delete`` in your :ref:`detail-allowed-methods`
            setting.

        Substitute appropriate names for ``objects`` and
        ``deleted_objects`` if ``Meta.collection_name`` is set to something
        other than ``objects`` (default).
        """
        request = convert_post_to_patch(request)
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        collection_name = self._meta.collection_name
        deleted_collection_name = 'deleted_%s' % collection_name
        if collection_name not in deserialized:
            raise BadRequest("Invalid data sent: missing '%s'" % collection_name)

        if len(deserialized[collection_name]) and 'put' not in self._meta.detail_allowed_methods:
            raise ImmediateHttpResponse(response=http.HttpMethodNotAllowed())

        bundles_seen = []

        for data in deserialized[collection_name]:
            # If there's a resource_uri then this is either an
            # update-in-place or a create-via-PUT.
            if "resource_uri" in data:
                uri = data.pop('resource_uri')

                try:
                    obj = self.get_via_uri(uri, request=request)

                    # The object does exist, so this is an update-in-place.
                    bundle = self.build_bundle(obj=obj, request=request)
                    bundle = self.full_dehydrate(bundle, for_list=True)
                    bundle = self.alter_detail_data_to_serialize(request, bundle)
                    self.update_in_place(request, bundle, data)
                except (ObjectDoesNotExist, MultipleObjectsReturned):
                    # The object referenced by resource_uri doesn't exist,
                    # so this is a create-by-PUT equivalent.
                    data = self.alter_deserialized_detail_data(request, data)
                    bundle = self.build_bundle(data=dict_strip_unicode_keys(data), request=request)
                    self.obj_create(bundle=bundle)
            else:
                # There's no resource URI, so this is a create call just
                # like a POST to the list resource.
                data = self.alter_deserialized_detail_data(request, data)
                bundle = self.build_bundle(data=dict_strip_unicode_keys(data), request=request)
                self.obj_create(bundle=bundle)

            bundles_seen.append(bundle)

        deleted_collection = deserialized.get(deleted_collection_name, [])

        if deleted_collection:
            if 'delete' not in self._meta.detail_allowed_methods:
                raise ImmediateHttpResponse(response=http.HttpMethodNotAllowed())

            for uri in deleted_collection:
                obj = self.get_via_uri(uri, request=request)
                bundle = self.build_bundle(obj=obj, request=request)
                self.obj_delete(bundle=bundle)

        if not self._meta.always_return_data:
            return http.HttpAccepted()
        else:
            to_be_serialized = {
                'objects': [
                    self.full_dehydrate(b, for_list=True)
                    for b in bundles_seen
                ]
            }
            to_be_serialized = self.alter_list_data_to_serialize(request, to_be_serialized)
            return self.create_response(request, to_be_serialized, response_class=http.HttpAccepted)

    def patch_detail(self, request, **kwargs):
        """
        Updates a resource in-place.

        Calls ``obj_update``.

        If the resource is updated, return ``HttpAccepted`` (202 Accepted).
        If the resource did not exist, return ``HttpNotFound`` (404 Not Found).
        """
        request = convert_post_to_patch(request)
        basic_bundle = self.build_bundle(request=request)

        # We want to be able to validate the update, but we can't just pass
        # the partial data into the validator since all data needs to be
        # present. Instead, we basically simulate a PUT by pulling out the
        # original data and updating it in-place.
        # So first pull out the original object. This is essentially
        # ``get_detail``.
        try:
            obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return http.HttpNotFound()
        except MultipleObjectsReturned:
            return http.HttpMultipleChoices("More than one resource is found at this URI.")

        bundle = self.build_bundle(obj=obj, request=request)
        bundle = self.full_dehydrate(bundle)
        bundle = self.alter_detail_data_to_serialize(request, bundle)

        # Now update the bundle in-place.
        deserialized = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))
        self.update_in_place(request, bundle, deserialized)

        if not self._meta.always_return_data:
            return http.HttpAccepted()
        else:
            # Invalidate prefetched_objects_cache for bundled object
            # because we might have changed a prefetched field
            bundle.obj._prefetched_objects_cache = {}
            bundle = self.full_dehydrate(bundle)
            bundle = self.alter_detail_data_to_serialize(request, bundle)
            return self.create_response(request, bundle, response_class=http.HttpAccepted)

    def update_in_place(self, request, original_bundle, new_data):
        """
        Update the object in original_bundle in-place using new_data.
        """
        original_bundle.data.update(**dict_strip_unicode_keys(new_data))

        # Now we've got a bundle with the new data sitting in it and we're
        # we're basically in the same spot as a PUT request. SO the rest of this
        # function is cribbed from put_detail.
        self.alter_deserialized_detail_data(request, original_bundle.data)
        kwargs = {
            self._meta.detail_uri_name: self.get_bundle_detail_data(original_bundle),
            'request': request,
        }
        return self.obj_update(bundle=original_bundle, **kwargs)

    def get_schema(self, request, **kwargs):
        """
        Returns a serialized form of the schema of the resource.

        Calls ``build_schema`` to generate the data. This method only responds
        to HTTP GET.

        Should return a HttpResponse (200 OK).
        """
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)
        self.log_throttled_access(request)
        bundle = self.build_bundle(request=request)
        self.authorized_read_detail(self.get_object_list(bundle.request), bundle)
        return self.create_response(request, self.build_schema())

    def get_multiple(self, request, **kwargs):
        """
        Returns a serialized list of resources based on the identifiers
        from the URL.

        Calls ``obj_get`` to fetch only the objects requested. This method
        only responds to HTTP GET.

        Should return a HttpResponse (200 OK).
        """
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Rip apart the list then iterate.
        kwarg_name = '%s_list' % self._meta.detail_uri_name
        obj_identifiers = kwargs.get(kwarg_name, '').split(';')
        objects = []
        not_found = []
        base_bundle = self.build_bundle(request=request)

        for identifier in obj_identifiers:
            try:
                obj = self.obj_get(bundle=base_bundle, **{self._meta.detail_uri_name: identifier})
                bundle = self.build_bundle(obj=obj, request=request)
                bundle = self.full_dehydrate(bundle, for_list=True)
                objects.append(bundle)
            except (ObjectDoesNotExist, Unauthorized):
                not_found.append(identifier)

        object_list = {
            self._meta.collection_name: objects,
        }

        if len(not_found):
            object_list['not_found'] = not_found

        self.log_throttled_access(request)
        return self.create_response(request, object_list)


class ModelDeclarativeMetaclass(DeclarativeMetaclass):
    def __new__(cls, name, bases, attrs):
        meta = attrs.get('Meta')

        if meta and hasattr(meta, 'queryset'):
            setattr(meta, 'object_class', meta.queryset.model)

        new_class = super(ModelDeclarativeMetaclass, cls).__new__(cls, name, bases, attrs)
        include_fields = getattr(new_class._meta, 'fields', [])
        excludes = getattr(new_class._meta, 'excludes', [])
        field_names = list(new_class.base_fields.keys())

        for field_name in field_names:
            if field_name == 'resource_uri':
                continue
            if field_name in new_class.declared_fields:
                continue
            if len(include_fields) and field_name not in include_fields:
                del(new_class.base_fields[field_name])
            if len(excludes) and field_name in excludes:
                del(new_class.base_fields[field_name])

        # Add in the new fields.
        new_class.base_fields.update(new_class.get_fields(include_fields, excludes))

        if getattr(new_class._meta, 'include_absolute_url', True):
            if 'absolute_url' not in new_class.base_fields:
                new_class.base_fields['absolute_url'] = fields.CharField(attribute='get_absolute_url', readonly=True)
        elif 'absolute_url' in new_class.base_fields and 'absolute_url' not in attrs:
            del(new_class.base_fields['absolute_url'])

        return new_class


class BaseModelResource(Resource):
    """
    A subclass of ``Resource`` designed to work with Django's ``Models``.

    This class will introspect a given ``Model`` and build a field list based
    on the fields found on the model (excluding relational fields).

    Given that it is aware of Django's ORM, it also handles the CRUD data
    operations of the resource.
    """
    @classmethod
    def should_skip_field(cls, field):
        """
        Given a Django model field, return if it should be included in the
        contributed ApiFields.
        """
        # Ignore certain fields (related fields).
        if getattr(field, 'rel'):
            return True

        return False

    @classmethod
    def api_field_from_django_field(cls, f, default=fields.CharField):
        """
        Returns the field type that would likely be associated with each
        Django type.
        """
        result = default
        internal_type = f.get_internal_type()

        if internal_type == 'DateField':
            result = fields.DateField
        elif internal_type == 'DateTimeField':
            result = fields.DateTimeField
        elif internal_type in ('BooleanField', 'NullBooleanField'):
            result = fields.BooleanField
        elif internal_type in ('FloatField',):
            result = fields.FloatField
        elif internal_type in ('DecimalField',):
            result = fields.DecimalField
        elif internal_type in ('IntegerField', 'PositiveIntegerField', 'PositiveSmallIntegerField', 'SmallIntegerField', 'AutoField'):
            result = fields.IntegerField
        elif internal_type in ('FileField', 'ImageField'):
            result = fields.FileField
        elif internal_type == 'TimeField':
            result = fields.TimeField
        # TODO: Perhaps enable these via introspection. The reason they're not enabled
        #       by default is the very different ``__init__`` they have over
        #       the other fields.
        # elif internal_type == 'ForeignKey':
        #     result = ForeignKey
        # elif internal_type == 'ManyToManyField':
        #     result = ManyToManyField

        return result

    @classmethod
    def get_fields(cls, fields=None, excludes=None):
        """
        Given any explicit fields to include and fields to exclude, add
        additional fields based on the associated model.
        """
        final_fields = {}
        fields = fields or []
        excludes = excludes or []

        if not cls._meta.object_class:
            return final_fields

        for f in cls._meta.object_class._meta.fields:
            # If the field name is already present, skip
            if f.name in cls.base_fields:
                continue

            # If field is not present in explicit field listing, skip
            if fields and f.name not in fields:
                continue

            # If field is in exclude list, skip
            if excludes and f.name in excludes:
                continue

            if cls.should_skip_field(f):
                continue

            api_field_class = cls.api_field_from_django_field(f)

            kwargs = {
                'attribute': f.name,
                'help_text': f.help_text,
                'verbose_name': f.verbose_name,
            }

            if f.null is True:
                kwargs['null'] = True

            kwargs['unique'] = f.unique

            if not f.null and f.blank is True:
                kwargs['default'] = ''
                kwargs['blank'] = True

            if f.get_internal_type() == 'TextField':
                kwargs['default'] = ''

            if f.has_default():
                kwargs['default'] = f.default

            if getattr(f, 'auto_now', False):
                kwargs['default'] = f.auto_now

            if getattr(f, 'auto_now_add', False):
                kwargs['default'] = f.auto_now_add

            final_fields[f.name] = api_field_class(**kwargs)
            final_fields[f.name].instance_name = f.name

        return final_fields

    def check_filtering(self, field_name, filter_type='exact', filter_bits=None):
        """
        Given a field name, a optional filter type and an optional list of
        additional relations, determine if a field can be filtered on.

        If a filter does not meet the needed conditions, it should raise an
        ``InvalidFilterError``.

        If the filter meets the conditions, a list of attribute names (not
        field names) will be returned.
        """
        if filter_bits is None:
            filter_bits = []

        if field_name not in self._meta.filtering:
            raise InvalidFilterError("The '%s' field does not allow filtering." % field_name)

        # Check to see if it's an allowed lookup type.
        if self._meta.filtering[field_name] not in (ALL, ALL_WITH_RELATIONS):
            # Must be an explicit whitelist.
            if filter_type not in self._meta.filtering[field_name]:
                raise InvalidFilterError("'%s' is not an allowed filter on the '%s' field." % (filter_type, field_name))

        if self.fields[field_name].attribute is None:
            raise InvalidFilterError("The '%s' field has no 'attribute' for searching with." % field_name)

        # Check to see if it's a relational lookup and if that's allowed.
        if len(filter_bits):
            if not getattr(self.fields[field_name], 'is_related', False):
                raise InvalidFilterError("The '%s' field does not support relations." % field_name)

            if not self._meta.filtering[field_name] == ALL_WITH_RELATIONS:
                raise InvalidFilterError("Lookups are not allowed more than one level deep on the '%s' field." % field_name)

            # Recursively descend through the remaining lookups in the filter,
            # if any. We should ensure that all along the way, we're allowed
            # to filter on that field by the related resource.
            related_resource = self.fields[field_name].get_related_resource(None)
            return [self.fields[field_name].attribute] + related_resource.check_filtering(filter_bits[0], filter_type, filter_bits[1:])

        return [self.fields[field_name].attribute]

    def filter_value_to_python(self, value, field_name, filters, filter_expr,
            filter_type):
        """
        Turn the string ``value`` into a python object.
        """
        # Simple values
        value = string_to_python(value)

        # Split on ',' if not empty string and either an in or range filter.
        if filter_type in ('in', 'range') and len(value):
            if hasattr(filters, 'getlist'):
                value = []

                for part in filters.getlist(filter_expr):
                    value.extend(part.split(','))
            else:
                value = value.split(',')

        return value

    # 构建过滤规则
    def build_filters(self, filters=None, ignore_bad_filters=False):
        """
        Given a dictionary of filters, create the necessary ORM-level filters.

        Keys should be resource fields, **NOT** model fields.

        Valid values are either a list of Django filter types (i.e.
        ``['startswith', 'exact', 'lte']``), the ``ALL`` constant or the
        ``ALL_WITH_RELATIONS`` constant.
        """
        # At the declarative level:
        #     filtering = {
        #         'resource_field_name': ['exact', 'startswith', 'endswith', 'contains'],
        #         'resource_field_name_2': ['exact', 'gt', 'gte', 'lt', 'lte', 'range'],
        #         'resource_field_name_3': ALL,
        #         'resource_field_name_4': ALL_WITH_RELATIONS,
        #         ...
        #     }
        # Accepts the filters as a dict. None by default, meaning no filters.
        if filters is None:
            filters = {}

        qs_filters = {}

        if getattr(self._meta, 'queryset', None) is not None:
            # Get the possible query terms from the current QuerySet.
            query_terms = self._meta.queryset.query.query_terms
        else:
            query_terms = QUERY_TERMS
        if django.VERSION >= (1, 8) and GeometryField:
            query_terms = query_terms | set(GeometryField.class_lookups.keys())

        for filter_expr, value in filters.items():
            filter_bits = filter_expr.split(LOOKUP_SEP)
            field_name = filter_bits.pop(0)
            filter_type = 'exact'

            if field_name not in self.fields:
                # It's not a field we know about. Move along citizen.
                continue

            if len(filter_bits) and filter_bits[-1] in query_terms:
                filter_type = filter_bits.pop()

            try:
                lookup_bits = self.check_filtering(field_name, filter_type, filter_bits)
            except InvalidFilterError:
                if ignore_bad_filters:
                    continue
                else:
                    raise
            value = self.filter_value_to_python(value, field_name, filters, filter_expr, filter_type)

            db_field_name = LOOKUP_SEP.join(lookup_bits)
            qs_filter = "%s%s%s" % (db_field_name, LOOKUP_SEP, filter_type)
            qs_filters[qs_filter] = value

        return dict_strip_unicode_keys(qs_filters)
    # 对数据集合进行排序, ModelResource
    def apply_sorting(self, obj_list, options=None):
        """
        Given a dictionary of options, apply some ORM-level sorting to the
        provided ``QuerySet``.

        Looks for the ``order_by`` key and handles either ascending (just the
        field name) or descending (the field name with a ``-`` in front).

        The field name should be the resource field, **NOT** model field.
        """
        if options is None:
            options = {}

        parameter_name = 'order_by'
        # 如果既没有 order_by也没有sort_by 则直接返回数据集合
        # 如果使用 sort_by则提示用户使用 order_by
        if 'order_by' not in options:
            if 'sort_by' not in options:
                # Nothing to alter the order. Return what we've got.
                return obj_list
            else:
                warnings.warn("'sort_by' is a deprecated parameter. Please use 'order_by' instead.")
                parameter_name = 'sort_by'

        order_by_args = []
        # 如果出传递的 options 包含getlist方法,则调用该方法
        # 如果没有 getlist 方法,则直接获取 option 的 order_by值
        if hasattr(options, 'getlist'):
            order_bits = options.getlist(parameter_name)
        else:
            order_bits = options.get(parameter_name)
            # 如果 order_bits 不是数组或元祖,则构建新的数组
            if not isinstance(order_bits, (list, tuple)):
                order_bits = [order_bits]
        # 对每一个 order_by 参数进行处理
        for order_by in order_bits:
            # LOOKUP_SEP = '__',将每一个 order_by 参数使用'__'切分
            order_by_bits = order_by.split(LOOKUP_SEP)
            # 切分后的参数第一个作为字段名
            field_name = order_by_bits[0]
            order = ''
            # 如果 field_name 以'-'开头, 例如 '-start_date' 表示反向排序
            # 则把 field_name 改为start_date
            # order 设为'-'
            if order_by_bits[0].startswith('-'):
                field_name = order_by_bits[0][1:]
                order = '-'
            # 如果要进行排序的字段,不在字段列表中,则返回不存在字段
            if field_name not in self.fields:
                # It's not a field we know about. Move along citizen.
                raise InvalidSortError("No matching '%s' field for ordering on." % field_name)
            # 如果要排序的字段,不在定义的_meta.ordering 中返回不支持排序
            if field_name not in self._meta.ordering:
                raise InvalidSortError("The '%s' field does not allow ordering." % field_name)
            # 如果排序字段没有attribute属性则返回错误
            if self.fields[field_name].attribute is None:
                raise InvalidSortError("The '%s' field has no 'attribute' for ordering with." % field_name)
            # -start_date
            order_by_args.append("%s%s" % (order, LOOKUP_SEP.join([self.fields[field_name].attribute] + order_by_bits[1:])))

        return obj_list.order_by(*order_by_args)

    def apply_filters(self, request, applicable_filters):
        """
        An ORM-specific implementation of ``apply_filters``.

        The default simply applies the ``applicable_filters`` as ``**kwargs``,
        but should make it possible to do more advanced things.
        """
        return self.get_object_list(request).filter(**applicable_filters)

    def get_object_list(self, request):
        """
        An ORM-specific implementation of ``get_object_list``.

        Returns a queryset that may have been limited by other overrides.
        """
        return self._meta.queryset._clone()

    def obj_get_list(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_get_list``.

        ``GET`` dictionary of bundle.request can be used to narrow the query.
        """
        filters = {}

        if hasattr(bundle.request, 'GET'):
            # Grab a mutable copy.
            filters = bundle.request.GET.copy()

        # Update with the provided kwargs.
        filters.update(kwargs)
        applicable_filters = self.build_filters(filters=filters)

        try:
            objects = self.apply_filters(bundle.request, applicable_filters)
            return self.authorized_read_list(objects, bundle)
        except ValueError:
            raise BadRequest("Invalid resource lookup data provided (mismatched type).")

    def obj_get(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_get``.

        Takes optional ``kwargs``, which are used to narrow the query to find
        the instance.
        """
        # Use ignore_bad_filters=True. `obj_get_list` filters based on
        # request.GET, but `obj_get` usually filters based on `detail_uri_name`
        # or data from a related field, so we don't want to raise errors if
        # something doesn't explicitly match a configured filter.
        applicable_filters = self.build_filters(filters=kwargs, ignore_bad_filters=True)
        if self._meta.detail_uri_name in kwargs:
            applicable_filters[self._meta.detail_uri_name] = kwargs[self._meta.detail_uri_name]

        try:
            object_list = self.apply_filters(bundle.request, applicable_filters)
            stringified_kwargs = ', '.join(["%s=%s" % (k, v) for k, v in applicable_filters.items()])

            if len(object_list) <= 0:
                raise self._meta.object_class.DoesNotExist("Couldn't find an instance of '%s' which matched '%s'." % (self._meta.object_class.__name__, stringified_kwargs))
            elif len(object_list) > 1:
                raise MultipleObjectsReturned("More than '%s' matched '%s'." % (self._meta.object_class.__name__, stringified_kwargs))

            bundle.obj = object_list[0]
            self.authorized_read_detail(object_list, bundle)
            return bundle.obj
        except ValueError:
            raise NotFound("Invalid resource lookup data provided (mismatched type).")

    def obj_create(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_create``.
        """
        bundle.obj = self._meta.object_class()

        for key, value in kwargs.items():
            setattr(bundle.obj, key, value)

        bundle = self.full_hydrate(bundle)
        return self.save(bundle)

    def lookup_kwargs_with_identifiers(self, bundle, kwargs):
        """
        Kwargs here represent uri identifiers Ex: /repos/<user_id>/<repo_name>/
        We need to turn those identifiers into Python objects for generating
        lookup parameters that can find them in the DB
        """
        lookup_kwargs = {}
        bundle.obj = self.get_object_list(bundle.request).model()
        # Override data values, we rely on uri identifiers
        bundle.data.update(kwargs)
        # We're going to manually hydrate, as opposed to calling
        # ``full_hydrate``, to ensure we don't try to flesh out related
        # resources & keep things speedy.
        bundle = self.hydrate(bundle)

        for identifier in kwargs:
            if identifier == self._meta.detail_uri_name:
                lookup_kwargs[identifier] = kwargs[identifier]
                continue

            field_object = self.fields[identifier]

            # Skip readonly or related fields.
            if field_object.readonly or field_object.is_related or\
                    not field_object.attribute:
                continue

            # Check for an optional method to do further hydration.
            method = getattr(self, "hydrate_%s" % identifier, None)

            if method:
                bundle = method(bundle)

            lookup_kwargs[identifier] = field_object.hydrate(bundle)

        return lookup_kwargs

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        """
        A ORM-specific implementation of ``obj_update``.
        """
        bundle_detail_data = self.get_bundle_detail_data(bundle)
        arg_detail_data = kwargs.get(self._meta.detail_uri_name)

        if bundle_detail_data is None or (arg_detail_data is not None and str(bundle_detail_data) != str(arg_detail_data)):
            try:
                lookup_kwargs = self.lookup_kwargs_with_identifiers(bundle, kwargs)
            except:
                # if there is trouble hydrating the data, fall back to just
                # using kwargs by itself (usually it only contains a "pk" key
                # and this will work fine.
                lookup_kwargs = kwargs

            try:
                bundle.obj = self.obj_get(bundle=bundle, **lookup_kwargs)
            except ObjectDoesNotExist:
                raise NotFound("A model instance matching the provided arguments could not be found.")

        bundle = self.full_hydrate(bundle)
        return self.save(bundle, skip_errors=skip_errors)

    def obj_delete_list(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_delete_list``.
        """
        objects_to_delete = self.obj_get_list(bundle=bundle, **kwargs)
        deletable_objects = self.authorized_delete_list(objects_to_delete, bundle)

        if hasattr(deletable_objects, 'delete'):
            # It's likely a ``QuerySet``. Call ``.delete()`` for efficiency.
            deletable_objects.delete()
        else:
            for authed_obj in deletable_objects:
                authed_obj.delete()

    def obj_delete_list_for_update(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_delete_list_for_update``.
        """
        objects_to_delete = self.obj_get_list(bundle=bundle, **kwargs)
        deletable_objects = self.authorized_update_list(objects_to_delete, bundle)

        if hasattr(deletable_objects, 'delete'):
            # It's likely a ``QuerySet``. Call ``.delete()`` for efficiency.
            deletable_objects.delete()
        else:
            for authed_obj in deletable_objects:
                authed_obj.delete()

    def obj_delete(self, bundle, **kwargs):
        """
        A ORM-specific implementation of ``obj_delete``.

        Takes optional ``kwargs``, which are used to narrow the query to find
        the instance.
        """
        if not hasattr(bundle.obj, 'delete'):
            try:
                bundle.obj = self.obj_get(bundle=bundle, **kwargs)
            except ObjectDoesNotExist:
                raise NotFound("A model instance matching the provided arguments could not be found.")

        self.authorized_delete_detail(self.get_object_list(bundle.request), bundle)
        bundle.obj.delete()

    @atomic_decorator()
    def patch_list(self, request, **kwargs):
        """
        An ORM-specific implementation of ``patch_list``.

        Necessary because PATCH should be atomic (all-success or all-fail)
        and the only way to do this neatly is at the database level.
        """
        return super(BaseModelResource, self).patch_list(request, **kwargs)

    def rollback(self, bundles):
        """
        A ORM-specific implementation of ``rollback``.

        Given the list of bundles, delete all models pertaining to those
        bundles.
        """
        for bundle in bundles:
            if bundle.obj and self.get_bundle_detail_data(bundle):
                bundle.obj.delete()

    def create_identifier(self, obj):
        return u"%s.%s.%s" % (obj._meta.app_label, get_module_name(obj._meta), obj.pk)

    def save(self, bundle, skip_errors=False):
        if bundle.via_uri:
            return bundle

        self.is_valid(bundle)

        if bundle.errors and not skip_errors:
            raise ImmediateHttpResponse(response=self.error_response(bundle.request, bundle.errors))

        # Check if they're authorized.
        if bundle.obj.pk:
            self.authorized_update_detail(self.get_object_list(bundle.request), bundle)
        else:
            self.authorized_create_detail(self.get_object_list(bundle.request), bundle)

        # Save FKs just in case.
        self.save_related(bundle)

        # Save the main object.
        obj_id = self.create_identifier(bundle.obj)

        if obj_id not in bundle.objects_saved or bundle.obj._state.adding:
            bundle.obj.save()
            bundle.objects_saved.add(obj_id)

        # Now pick up the M2M bits.
        m2m_bundle = self.hydrate_m2m(bundle)
        self.save_m2m(m2m_bundle)
        return bundle

    def save_related(self, bundle):
        """
        Handles the saving of related non-M2M data.

        Calling assigning ``child.parent = parent`` & then calling
        ``Child.save`` isn't good enough to make sure the ``parent``
        is saved.

        To get around this, we go through all our related fields &
        call ``save`` on them if they have related, non-M2M data.
        M2M data is handled by the ``ModelResource.save_m2m`` method.
        """
        for field_name, field_object in self.fields.items():
            if not field_object.is_related:
                continue

            if field_object.is_m2m:
                continue

            if not field_object.attribute:
                continue

            if field_object.readonly:
                continue

            if field_object.blank and field_name not in bundle.data:
                continue

            # Get the object.
            try:
                related_obj = getattr(bundle.obj, field_object.attribute)
            except ObjectDoesNotExist:
                # Django 1.8: unset related objects default to None, no error
                related_obj = None

            # We didn't get it, so maybe we created it but haven't saved it
            if related_obj is None:
                related_obj = bundle.related_objects_to_save.get(field_object.attribute, None)

            if related_obj and field_object.related_name:
                # this might be a reverse relation, so we need to save this
                # model, attach it to the related object, and save the related
                # object.
                if not self.get_bundle_detail_data(bundle):
                    bundle.obj.save()

                setattr(related_obj, field_object.related_name, bundle.obj)

            related_resource = field_object.get_related_resource(related_obj)

            # Before we build the bundle & try saving it, let's make sure we
            # haven't already saved it.
            if related_obj:
                obj_id = self.create_identifier(related_obj)

                if obj_id in bundle.objects_saved:
                    # It's already been saved. We're done here.
                    continue

            if bundle.data.get(field_name):
                if hasattr(bundle.data[field_name], 'keys'):
                    # Only build & save if there's data, not just a URI.
                    related_bundle = related_resource.build_bundle(
                        obj=related_obj,
                        data=bundle.data.get(field_name),
                        request=bundle.request,
                        objects_saved=bundle.objects_saved
                    )
                    related_resource.full_hydrate(related_bundle)
                    related_resource.save(related_bundle)
                    related_obj = related_bundle.obj
                elif field_object.related_name:
                    # This condition probably means a URI for a reverse
                    # relation was provided.
                    related_bundle = related_resource.build_bundle(
                        obj=related_obj,
                        request=bundle.request,
                        objects_saved=bundle.objects_saved
                    )
                    related_resource.save(related_bundle)
                    related_obj = related_bundle.obj

            if related_obj:
                setattr(bundle.obj, field_object.attribute, related_obj)

    def save_m2m(self, bundle):
        """
        Handles the saving of related M2M data.

        Due to the way Django works, the M2M data must be handled after the
        main instance, which is why this isn't a part of the main ``save`` bits.

        Currently slightly inefficient in that it will clear out the whole
        relation and recreate the related data as needed.
        """
        for field_name, field_object in self.fields.items():
            if not field_object.is_m2m:
                continue

            if not field_object.attribute:
                continue

            if field_object.readonly:
                continue

            # Get the manager.
            related_mngr = None

            if isinstance(field_object.attribute, six.string_types):
                related_mngr = getattr(bundle.obj, field_object.attribute)
            elif callable(field_object.attribute):
                related_mngr = field_object.attribute(bundle)

            if not related_mngr:
                continue

            if hasattr(related_mngr, 'clear'):
                # FIXME: Dupe the original bundle, copy in the new object &
                #        check the perms on that (using the related resource)?

                # Clear it out, just to be safe.
                related_mngr.clear()

            related_objs = []

            for related_bundle in bundle.data[field_name]:
                related_resource = field_object.get_related_resource(bundle.obj)

                # Only build & save if there's data, not just a URI.
                updated_related_bundle = related_resource.build_bundle(
                    obj=related_bundle.obj,
                    data=related_bundle.data,
                    request=bundle.request,
                    objects_saved=bundle.objects_saved,
                    via_uri=related_bundle.via_uri,
                )

                related_resource.save(updated_related_bundle)
                related_objs.append(updated_related_bundle.obj)

            related_mngr.add(*related_objs)


class ModelResource(six.with_metaclass(ModelDeclarativeMetaclass, BaseModelResource)):
    pass


class NamespacedModelResource(ModelResource):
    """
    A ModelResource subclass that respects Django namespaces.
    """
    def _build_reverse_url(self, name, args=None, kwargs=None):
        namespaced = "%s:%s" % (self._meta.urlconf_namespace, name)
        return reverse(namespaced, args=args, kwargs=kwargs)


# Based off of ``piston.utils.coerce_put_post``. Similarly BSD-licensed.
# And no, the irony is not lost on me.
def convert_post_to_VERB(request, verb):
    """
    Force Django to process the VERB.
    """
    if request.method == verb:
        if hasattr(request, '_post'):
            del request._post
            del request._files

        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = verb
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = verb
        setattr(request, verb, request.POST)

    return request


def convert_post_to_put(request):
    return convert_post_to_VERB(request, verb='PUT')


def convert_post_to_patch(request):
    return convert_post_to_VERB(request, verb='PATCH')
```

每个 api 有4个view

- ^api/ ^(?P<api_name>v1)/ ^(?P<resource_name>accounting_standard)/$ [name='api_dispatch_list']
- ^api/ ^(?P<api_name>v1)/ ^(?P<resource_name>accounting_standard)/schema/$ [name='api_get_schema']
- ^api/ ^(?P<api_name>v1)/ ^(?P<resource_name>accounting_standard)/set/(?P<pk_list>.*?)/$ [name='api_get_multiple']
- ^api/ ^(?P<api_name>v1)/ ^(?P<resource_name>accounting_standard)/(?P<pk>.*?)/$ [name='api_dispatch_detail']


### 开始

#### 创建资源

这里我们在Api/api.py创建一个资源

```python
from tastypie.resources import ModelResource
from account.models import User

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
```

上面建立了新的资源,EntryResource会自动建立所有的非关联字段,这些字段会关联到User的字段上;Meta中的resource_name是可选的,如果没有提供,那么默认为类名去掉Resource之后的小写字符串(`UserResource.__name__[:-8].**class**lower()`).

这个resource_name用来澄清,URL中对应资源名称,这里社否设置无关紧要.

#### 创建关联字段

因为tastypie不知道开发者会如何展示数据,所以没有对关联字段自动进行关联.例如user的group_ids无法进行关联

解决方法:创建一个GroupResource资源

```python
from tastypie import fields
from tastypie.resources import ModelResource
from account.models import User, Group

class GroupResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'

class UserResource(ModelResource):
    group_ids=fields.Many2Many(GroupResource,'group_ids')
    # 这里的第一个group_ids是tastypie的字段名,第二个group_ids是告诉tastypie,User表使用group_ids关联到GroupResource.
    # 这里的两个名字不必相同
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()
```
对于当个资源添加url

```python
entry_resource = EntryResource()
urlpatterns = [
    url(r'^api/', include(entry_resource.urls)),
]
```

#### 将资源通过api暴露出来

```python
from django.conf.urls import url, include
from tastypie.api import Api
from myapp.api import EntryResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(EntryResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
]
```

在外部会看到api/v1/`resource_name`/的资源URL

#### 限制数据访问

禁止访问的字段,这里是使用黑名单禁止.

```python
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
```

还可以使用白名单来允许.

```python
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        fields = ['username', 'first_name', 'last_name', 'last_login']
```

限制访问方式

```python
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']
```

### 与API交互

假设有下面的接口

```python
# myapp/api/resources.py
from django.contrib.auth.models import User
from tastypie.authorization import Authorization
from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from myapp.models import Entry


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        filtering = {
            'username': ALL,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],

        }


class EntryResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        queryset = Entry.objects.all()
        resource_name = 'entry'
        authorization = Authorization()
        filtering = {
            'user': ALL_WITH_RELATIONS,
            'pub_date': ['exact', 'lt', 'lte', 'gte', 'gt'],
        }


# urls.py
from django.conf.urls import url, include
from tastypie.api import Api
from myapp.api.resources import EntryResource, UserResource

v1_api = Api(api_name='v1')
v1_api.register(UserResource())
v1_api.register(EntryResource())

urlpatterns = [
    # The normal jazz here...
    url(r'^blog/', include('myapp.urls')),
    url(r'^api/', include(v1_api.urls)),
]
```

调用`curl http://localhost:8000/api/v1/`返回当前api接口下所有的资源

```javascript
{
    "entry": {
        "list_endpoint": "/api/v1/entry/",
        "schema": "/api/v1/entry/schema/"
    },
    "user": {
        "list_endpoint": "/api/v1/user/",
        "schema": "/api/v1/user/schema/"
    }
}
```

`curl http://localhost:8000/api/v1/?fullschema=true`获取所有信息

```javascript
{
    "entry": {
        "list_endpoint": "/api/v1/entry/",
        "schema": {
            "default_format": "application/json",
            "fields": {
                "body": {
                    "help_text": "Unicode string data. Ex: \"Hello World\"",
                    "nullable": false,
                    "readonly": false,
                    "type": "string"
                },
                ...
            },
            "filtering": {
                "pub_date": ["exact", "lt", "lte", "gte", "gt"],
                "user": 2
            }
        }
    },
}
```
如果想要获取指定的资源,例如获取id为1,2,4的资源,可用`curl http://localhost:8000/api/v1/user/set/1;2;4`

使用post创建对象时的返回头为

```shell
# 创建一个资源POST
curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"body": "This will prbbly be my lst post.", "pub_date": "2011-05-22T00:46:38", "slug": "another-post", "title": "Another Post", "user": "/api/v1/user/1/"}' http://localhost:8000/api/v1/entry/

# 这里使用了--dump-header.如果发生错误时这里的返回头信息会有帮助

HTTP/1.0 201 CREATED
Date: Fri, 20 May 2011 06:48:36 GMT
Server: WSGIServer/0.1 Python/2.7
Content-Type: text/html; charset=utf-8
Location: http://localhost:8000/api/v1/entry/4/

# 更新一条资源PUT
curl --dump-header - -H "Content-Type: application/json" -X PUT --data '{"body": "This will probably be my last post.", "pub_date": "2011-05-22T00:46:38", "slug": "another-post", "title": "Another Post", "user": "/api/v1/user/1/"}' http://localhost:8000/api/v1/entry/4/
After fixing up the body, we get back:

HTTP/1.0 204 NO CONTENT
Date: Fri, 20 May 2011 07:13:21 GMT
Server: WSGIServer/0.1 Python/2.7
Content-Length: 0
Content-Type: text/html; charset=utf-8

# 部分更新PATCH
curl --dump-header - -H "Content-Type: application/json" -X PATCH --data '{"body": "This actually is my last post."}' http://localhost:8000/api/v1/entry/4/
To which we should get back:

HTTP/1.0 202 ACCEPTED
Date: Fri, 20 May 2011 07:13:21 GMT
Server: WSGIServer/0.1 Python/2.7
Content-Length: 0
Content-Type: text/html; charset=utf-8

更新多条数据PUT
curl --dump-header - -H "Content-Type: application/json" -X PUT --data '{"objects": [{"body": "Welcome to my blog!","id": "1","pub_date": "2011-05-20T00:46:38","resource_uri": "/api/v1/entry/1/","slug": "first-post","title": "First Post","user": "/api/v1/user/1/"},{"body": "I'm really excited to get started with this new blog. It's gonna be great!","id": "3","pub_date": "2011-05-20T00:47:30","resource_uri": "/api/v1/entry/3/","slug": "my-blog","title": "My Blog","user": "/api/v1/user/2/"}]}' http://localhost:8000/api/v1/entry/

# 删除一条资源
curl --dump-header - -H "Content-Type: application/json" -X DELETE  http://localhost:8000/api/v1/entry/4/
Once again, we get back the “Accepted” response of a 204:

HTTP/1.0 204 NO CONTENT
Date: Fri, 20 May 2011 07:28:01 GMT
Server: WSGIServer/0.1 Python/2.7
Content-Length: 0
Content-Type: text/html; charset=utf-8

# 删除整个资源
curl --dump-header - -H "Content-Type: application/json" -X DELETE  http://localhost:8000/api/v1/entry/
As a response, we get:

HTTP/1.0 204 NO CONTENT
Date: Fri, 20 May 2011 07:32:51 GMT
Server: WSGIServer/0.1 Python/2.7
Content-Length: 0
Content-Type: text/html; charset=utf-8

# 执行多个操作,这了执行了创建和删除
curl --dump-header - -H "Content-Type: application/json" -X PATCH --data '{"objects": [{"body": "Surprise! Another post!.", "pub_date": "2012-02-16T00:46:38", "slug": "yet-another-post", "title": "Yet Another Post"}], "deleted_objects": ["http://localhost:8000/api/v1/entry/4/"]}'  http://localhost:8000/api/v1/entry/

HTTP/1.0 202 ACCEPTED
Date: Fri, 16 Feb 2012 00:46:38 GMT
Server: WSGIServer/0.1 Python/2.7
Content-Length: 0
Content-Type: text/html; charset=utf-8
```

删除所有数据`delete api/v1/user/`
## 状态码
- 201 创建成功
- 204 PUT更新成功,DELETE成功
- 202 PATCH更细成功
- 404 DELETE失败,
## Tastypie 设置

### API_LIMIT_PER_PAGE 可选 默认20

设置默认情况下列表显示的数据量,这样就不需要使用limit来指定

### TASTYPIE_FULL_DEBUG 可选 默认False

控制异常情况下的处理方式,如果True,而且django的DEBUG=true,那么使用标准django的500.如果False,当DEBUG=True会得到确切的错误信息,当DEBUG=False时,Tasypie会调用`mail_admins()`方法并且提供canned消息(canned可以使用TASTYPIE_CANNED_ERROR来重写)

### TASTYPIE_CANNED_ERROR 可选

例如`TASTYPIE_CANNED_ERROR = "Oops, we broke it!"`

### TASTYPIE_ALLOW_MISSING_SLASH 可选 默认False

允许URL结尾不用`\`,必须和`settings.APPEND_SLASH = False`一起使用这样django就不会触发302

### TASTYPIE_DATETIME_FORMATTING 可选 默认iso-8601\. iso-8601

设置时间的默认格式

### TASTYPIE_DEFAULT_FORMATS 可选 默认['json', 'xml', 'yaml', 'plist']

设置tastypie的可选数据格式,例如:TASTYPIE_DEFAULT_FORMATS = ['json', 'xml']

### TASTYPIE_ABSTRACT_APIKEY 可选 默认False

此设置使ApiKey模型成为抽象基类。 这在多数据库设置中可能是有用的，其中许多数据库都有自己的用户数据表和ApiKeyAuthentication不被使用。 没有此设置，必须在包含用户帐户数据的每个数据库（如django.contrib.auth.models.User生成的Django内置auth_user表）中创建tastypie_apikey表。

## 使用Tastypie做非ORM数据的资源

实际上tastypie都是在`Resource`类中处理请求和返回值.`ModelResource`只是在`Resource`上做了封装来处理ORM数据.我们只需要修改`ModelResource`处理ORM数据的方法,就可来处理非ORM的数据.

## 测试

## 资源

Tastypie的request/response是标准的django行为,例如请求`/api/v1/user/?format=json`:

1. Resource.urls 会被django的url规则检测
2. 在匹配view列表时,`Resource.wrap_view('dispatch_list')`会被调用,它提供了基础的错误处理并且允许返回序列化的错误信息
3. 因为`dispatch_list`传递给了`wrap_view`,所以`Resource.dispatch_list`是下一个被调用的方法.This is a thin wrapper around `Resource.dispatch`
4. `dispatch`做了很多事,她确认一下几件事:

  1. http请求方法在`allowed_methods`里面(`method_check`)
  2. class有有一个方法可以处理请求(`get_list`)
  3. 用户被授权(`is_authenticated`)
  4. 用户没有超出请求次数限制(`throttle_check`)

5. `request`做了api下真正的工作:

  1. 通过`Resource.obj_get_list`获取可用的对象.对于`ModelResource`她使用`ModelResource.build_filters`来执行ORM过滤条件,然后过`ModelResource.get_object_list`来返回`QuerySet`,然后把orm过滤条件应用到`QuerySet`上面.
  2. 然后基于用户的输入来对对象进行排序(`ModelResource.apply_sorting`)
  3. 然后使用`Paginator`进行分页,然后把数据进行序列化.
  4. 页中的每一个对象应用了`full_dehydrate`,这样Tastypie就可以将原始数据转化为,`endpoint`支持的字段
  5. 最终他调用`Resource.create_response`

6. `create_response`是一个快捷方法:

  1. 确认需要返回的数据格式(`Resource.determine_format`)
  2. 将数据按照格式序列化
  3. 使用django的`HttpResponse`(200OK)来返回数据

7. 我们把调用栈交给`dispatch`.还有一个`dispatch`可能做得是保存请求信息来做请求限制(`Resource.log_throttled_access`), 然后返回一个`HttpResponse`,这样django就不会退出

处理其他`endpoint`或者HTTP请求方法的过程与上面这个一致,`<http_method>_<list_or_detail>`.在`PUT/POST`中需要额外调用`hydrate`流程,她用来处理获取用户数据,并将数据转变为用于存储的原始数据

## 为什么使用URI

尽管可以使用`full=True`来将关联字段的所有数据展示,但是默认是使用URI.URI也很容易缓存.

## 访问当前的请求

根据当前的请求来改变行为是非常普遍的需求.事实上在`Resource/ModelResource`中,只要`bundle`可见,就可以用`bundle.request`.

`override/extend`的可以将`bundle`参数传递给他

如果使用`Resource/ModelResource`是`request`不可用,那么会有一个空的`Request`.如果在你的代码中这是一个常见的`pattern/usage`,那么你可能需要为不存在的数据做适配.

## 高级数据准备方式

并不是所有的数据都可以通过`object/model`的属性来获得.可能需要添加一些不在model上存在的数据.这里使用`dehydrate/hydrate`.

### Dehydrate过程

tastypie使用`Dehydrate`过程,将原始的复杂model数据转换成用户可以接受数据结构.这通常是将复杂的数据对象转换成包含简单数据结构的字典.

总体来说就是,获取`bundle.obj`对象并构建`bundle.data`

流程如下:

1. 将数据模型放到`Bundle`实例中,然后传递给多个函数.
2. 遍历资源的所有数据,对`bundle`上的每一个字段执行`Dehydrate`.
3. 当处理每一字段时,查找`dehydrate_<fieldname>`的方法,如果有就调用该方法.将`bundle`对象传递给他
4. 所有字段处理完后,如果`Resource`中有`dehydrate`,那么将完整的`bundle`传递给它.

这个流程的目的是将适合序列化的数据填充到`bundle.data`字典中.除了`alter_*`方法之外,这方法用于控制真正被序列化并且发送给客户端的内容.

### 每个字段的Dehydrate

每个字段有自己的`Dehydrate`方法.如果她知道如何获取数据(例如,指定字段的`attribute`参数),那么他会根据attribute尝试自动填充.

返回值会通过字段名插入到`bundle.data`字典中

### dehydrate_FOO

因为不是所有数据都可以直接通过属性来获取(例如,通过函数/查询),不论字段如何产生的,使用这个字段都可以向其中填充数据或消息

这里的`FOO`不是字面意思,他是一个占位符,应该被替换为字段名称

例如:

```python
class MyResource(ModelResource):
    # The ``title`` field is already added to the class by ``ModelResource``
    # and populated off ``Note.title``. But we want allcaps titles...
    class Meta:
        queryset = Note.objects.all()

    def dehydrate_title(self, bundle):
        return bundle.data['title'].upper()

class MyResource(ModelResource):
    # As is, this is just an empty field. Without the ``dehydrate_rating``
    # method, no data would be populated for it.
    rating = fields.FloatField(readonly=True)

    class Meta:
        queryset = Note.objects.all()

    def dehydrate_rating(self, bundle):
        total_score = 0.0

        # Make sure we don't have to worry about "divide by zero" errors.
        if not bundle.obj.rating_set.count():
            return total_score

        # We'll run over all the ``Rating`` objects & calculate an average.
        for rating in bundle.obj.rating_set.all():
            total_score += rating.rating

        return total_score /  bundle.obj.rating_set.count()
    # 这里的返回值会更新bundle.data,不应该直接去修改bundle.data的值
```

### dehydrate

`dehydrate`函数接受完整的`bundle.data`,并且应用所有的数据修改.当一个数据可能依赖于多个数据字段时

```python
class MyResource(ModelResource):
    class Meta:
        queryset = Note.objects.all()

    def dehydrate(self, bundle):
        # Include the request IP in the bundle.
        bundle.data['request_ip'] = bundle.request.META.get('REMOTE_ADDR')
        return bundle
class MyResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        excludes = ['email', 'password', 'is_staff', 'is_superuser']

    def dehydrate(self, bundle):
        # If they're requesting their own record, add in their email address.
        if bundle.request.user.pk == bundle.obj.pk:
            # Note that there isn't an ``email`` field on the ``Resource``.
            # By this time, it doesn't matter, as the built data will no
            # longer be checked against the fields on the ``Resource``.
            bundle.data['email'] = bundle.obj.email

        return bundle
```

这个函数必须返回`bundle`对象,不管它改变现有数据还是添加一个新的数据.甚至可以删除`bundle.data`中的任何数据

### Hydrate 流程

Tastypie将用户发来的数据进行序列化,并将它转化为可用的数据模型.与`dehydrate`流程相反.

1. 将客户端数据放入`Bundle`对象中,那后交给其他函数.
2. 如果`hydrate`函数存在,就将完整的`bundle`对象传递给他
3. 当处理每一字段时,查找`hydrate_<fieldname>`的方法,如果有就调用该方法,将`bundle`对象传递给他
4. 当所有其他的处理完成时,让每一个字段调用自己的`hydrate`,并把`bundle`对象传递给他么

### hydrate

`hydrate`允许初始化`bundle.obj`

这个函数必须返回`bundle`对象,不管它改变现有数据还是添加一个新的数据.甚至可以删除`bundle.obj`中的任何数据

### hydrate_FOO

客户端传来的数据可能没有直接映射到数据模型上,这个方法,允许接受数据并且尽心修改

```python
class MyResource(ModelResource):
    # The ``title`` field is already added to the class by ``ModelResource``
    # and populated off ``Note.title``. But we want lowercase titles...

    class Meta:
        queryset = Note.objects.all()

    def hydrate_title(self, bundle):
        bundle.data['title'] = bundle.data['title'].lower()
        return bundle
```

每个字段都有自己的`hydrate`方法

## 反向关联关系

Tastypie没有像django一样提供了反向关联关系,当时tastypie使用`ToOneField`和`ToManyField`来

```python
# myapp/api/resources.py
from tastypie import fields
from tastypie.resources import ModelResource
from myapp.models import Note, Comment


class NoteResource(ModelResource):
    comments = fields.ToManyField('myapp.api.resources.CommentResource', 'comments')

    class Meta:
        queryset = Note.objects.all()


class CommentResource(ModelResource):
    note = fields.ToOneField(NoteResource, 'notes')

    class Meta:
        queryset = Comment.objects.all()
```

**和django不同的是Tastypie不可以直接用`'CommentResource'`,即使实在统一个module下**

Tastypie也支持`self-referential`字段

```python
# myapp/api/resources.py
from tastypie import fields
from tastypie.resources import ModelResource
from myapp.models import Note


class NoteResource(ModelResource):
    sub_notes = fields.ToManyField('self', 'notes')

    class Meta:
        queryset = Note.objects.all()
```

## 资源选项(AKA Meta)

内置的Meta类,允许对Resource进行配置

### serializer 默认`tastypie.serializers.Serializer()`

控制Resource应该使用哪一个class来做序列化

### authentication 默认`tastypie.authentication.Authentication()`

控制Resource应该使用哪一个class来做authentication

### authorization 默认 `tastypie.authorization.ReadOnlyAuthorization().`

控制Resource应该使用哪一个class来做authorization

### validation 默认 `tastypie.validation.Validation()`

控制Resource应该使用哪一个class来做validation

### paginator_class 默认 `tastypie.paginator.Paginator`

控制Resource应该使用哪一个class来做paginator_class

### cache 默认 `tastypie.validation.NoCache()`

控制Resource应该使用哪一个class来做cache

### throttle 默认 `tastypie.validation.BaseThrottle()`

控制Resource应该使用哪一个class来做 throttle

### allowed_methods 默认 None

控制Resource可以响应的list和detail请求方法,默认None,这意味着交给`list_allowed_methods`和`detail_allowed_methods`这两个选项.

### list_allowed_methods

控制Resource可以响应的list请求方法,默认`['get', 'post', 'put', 'delete', 'patch']`

### detail_allowed_methods

控制Resource可以响应的detail请求方法,默认`['get', 'post', 'put', 'delete', 'patch']`

### limit

空每次请求返回的结果数目,默认为20或者时`API_LIMIT_PER_PAGE`设置的值

### api_name

当创建资源的urls覆盖资源,默认None

### resource_name

资源名称如果没有提供,则使用类名的小写

### default_format

设置默认的数据格式,默认为json

### filtering

是一个字典,字典的key是用户可以进行过滤的字段,value为用户过滤字段时可以使用的方法

### ordering

设置哪些字段用户可以进行排序

### object_class

设置给Resource提供数据的class,在ModelResource中是queryset就model class

### fields

用户可访问字段的白名单

### excludes

用户可访问字段的黑名单

### include_resource_uri

指当用`get_absolute_url`获取对象时,定是否需要包含额外的字段,默认False

### always_return_data

规定HTTP除了(DELETE)方法外,都要返回序列化数据,默认False

### collection_name

当使用get获取list时,list的名称,默认是`objects`

## 基础过滤

ModelResource提供了基础的Django Orm过滤接口.

```python
from tastypie.constants import ALL, ALL_WITH_RELATIONS
class MyResource(ModelResource):
    class Meta:
        filtering = {
            "slug": ('exact', 'startswith',),
            "title": ALL,
        }
```

上面规定slug字段允许使用`'exact', 'startswith'`两个过滤条件,title有可使用所有过滤条件

## 高级过滤

使用高级的过滤你可能使用`build_filters()`来自定义过滤

```python
from haystack.query import SearchQuerySet

class MyResource(Resource):
    def build_filters(self, filters=None):
        if filters is None:
            filters = {}

        orm_filters = super(MyResource, self).build_filters(filters)

        if "q" in filters:
            sqs = SearchQuerySet().auto_query(filters['q'])

            orm_filters["pk__in"] = [i.pk for i in sqs]

        return orm_filters
```

## 对于不支持使用PUT/DELETE/PATCH的场景

使用`X-HTTP-Method-Override`替换 例如`curl --dump-header - -H "Content-Type: application/json" -H "X-HTTP-Method-Override: PATCH" -X POST --data '{"title": "I Visited Grandma Today"}' http://localhost:8000/api/v1/entry/1/`

## Resource 方法

### Resource.wrap_view(self, view)

包装函数,例如可以更好的处理异常

### Resource.get_response_class_for_exception(self, request, exception)

必须返回django HttpResponse,可以覆盖自定义用于未捕获异常的响应类

### Resource.base_urls

这个Resource应该响应的标准URL 。这些包括默认list,detail，schema和多个endpoit。必须返回一个url列表

### Resource.prepend_urls

一个钩子，用于添加您自己的URL或在默认URL之前进行匹配。用于添加自定义endpoint或覆盖内置的（从base_urls）。

### Resource.urls

Resource的urls,组合base_urls与override_urls.大多数是一个标准的URLconf，这适合于在注册一个Api类时自动使用，或者直接包含在URLconf中

### Resource.determine_format

用于确定所需的格式

### Resource.serialize

对给定的数据进行序列化

### Resource.deserialize

对给定的请求.数据,类型进行反序列化.依赖于请求的`CONTENT_TYPE`头

### Resource.alter_list_data_to_serialize

在数据列表进行序列话并且发送给用户之前进行数据修改

### Resource.alter_detail_data_to_serialize
在数据详情进行序列话并且发送给用户之前进行数据修改

### Resource.alter_deserialized_list_data
在数据列表从用户端接受到并反序列化之前修改数据

### Resource.alter_deserialized_detail_data

在数据详细从用户端接受到并反序列化之前修改数据,在hydration之前很有用

### Resource.dispatch_list
对于数据列表,处理各种HTTP请求方法,依赖于`Resource.dispatch`

### Resource.dispatch_detail

对于数据详情,处理各种HTTP请求方法,依赖于`Resource.dispatch`

### Resource.dispatch
处理通常的操作(allowed HTTP method, authentication, throttling, method lookup)

### Resource.remove_api_resource_names
给出一个来自URLconf的模式匹配字典,如果有移除api_name and/or resource_name

### Resource.method_check
检查请求方法是否允许

### Resource.is_authenticated
检查是否authenticated,它使用Meta设置中的authentication

### throttle_check
检查用户是否应该被限制

### Resource.log_throttled_access
处理用户访问的记录,用于限制用户访问.它使用Meta中的`throttle`

### build_bundle
传递一个对象或者一个数据字典,给后面的dehydrate/hydrate流程使用,如果没有提供对象,使用`Resource._meta.object_class`创建空对象

### get_bundle_detail_data


## Bundle
