# odoo development essential
## Index
- [Set up](#1)
- [Module]()
- [Inheritance]()
- [Data]()
- [Modle]()
- [View]()
- [ORM]()
- [QWeb]()
- [External Api]()
- [Deployment]()


## Set up
### install
#### instanll on debain/ubuntu   
1. $ git clone odoo_source
2. ./odoo.py setup_deps
3. ./odoo.py setup_pg

#### init database
1. createuser --superuser  
2. createdb v9dev  
3. ./odoo.py -d v9dev `[--without-demo-data=all]` 默认odoo会将测试数据加载，这个参数可以禁用
#### create database from  template
1. createdb --template=v9dev v9test
2. psql -l
3. dropdb v9test

> odoo 不同版本数据库是不兼容的  

### configuration files/options
默认情况下，odoo会将配置文件保存在用户目录下~/.openerp-serverrc  
--save 参数可以将当前的参数保存到~/.openerp-serverrc中  
`./odoo.py --save --stop-after-init`    
`--stop--after-init` 在初始化完成后停止，通常用来测试检查module安装升级。  
还可以指定配置文件`--conf=<filepath>`
### change xmlrpc port
可以修改`--xmlrpc-server=<port>`来修改默认的端口号，这样子可以在一台机器上运行多个实例。  
./odoo.py --xmlrpc-server=8090  
./odoo.py --xmlrpc-server=8091   

### logging
`--log-level`可以设置日志级别，默认odoo把日志打印到console中，`--logfile=<filepath>`可以将日志写到文件中。  

**--debug**当系统发生异常时，odoo会启动pdb。  

## odoo App
module和app是不同的，module是一个包涵__init__.py，还有__openerp.py的文件夹，app类似于HR等一些功能组织的中心，其它modules可以修改添加功能。  
### 修改和扩展modules
关于继承：通常不应该直接在原始模块上作修改，这样会破坏模块的结构，而是重新写一个模块。
### 创建新的module
upgrade ./odoo.py -d v9dev -u module_name `－u`可以直接更新moule,但是需要天际－d选项   
### 添加菜单
``` xml
<?xml version="1.0"?>
<openerp>
    <data>
    <act_window id="action_todo_task" name="To-do Task"
        res_model="todo.task"
        view_mode="tree,form"
    />
    <menuitem id="menu_todo_task"
        name="To-Do Tasks"
        parent="mail.mail_feeds"
        sequence="20"
        action="action_todo_task"
    />
    </data>
</openerp>
```
### View
odoo 提供了多种view，所有的view都保存在数据库中ir.model.view。在xml中定义view保存到数据库中。   

### 创建form
button中name是执行的函数名称，string是页面显示名称，type是button类型，class是Css样式
```xml
<record model="ir.ui.view" id="bps_billing_product_form_view">
      <field name="name">bps.billing.product.form</field>
      <field name="model">bps.billing.product</field>
      <field name="type">form</field>
      <field name="arch" type="xml">
           <form string="基础产品">
                <header>
                    <button name="do_toggle_done" type="object"
                    string="Toggle Done" class="oe_highlight"/>
                </header>
                <sheet>
                    <group></group>
                </sheet>
           </form>
      </field>
</record>
```
### 创建list和search视图
```xml
<record model="ir.ui.view" id="bps_billing_product_tree_view">
   <field name="name">bps.billing.product.tree</field>
   <field name="model">bps.billing.product</field>
   <field name="type">tree</field>
   <field name="arch" type="xml">
       <tree string="基础产品">
           <field name="name"/>
       </tree>
   </field>
</record>
```
odoo 自带了一个搜索框，可以用search定义搜索框   
search 不需要添加type字段  
```xml
<record model="ir.ui.view" id="bps_billing_product_tree_view">
   <field name="name">bps.billing.product.tree</field>
   <field name="model">bps.billing.product</field>
   <field name="arch" type="xml">
       <search>
           <field name="name"/>
           <filter string="not done" domain="[('is_done','=',False)]">
           </filter>
       </search>
   </field>
</record>
```
### 添加业务逻辑
将逻辑绑定到button上面，
```python
@api.openerp
def do_toggle_done(self):
    self.is_done = not self.is_done
    return True
```
这里的函数名和button按钮的name是一样的

### model访问权限控制
`ir.model.access`  
需要在data中加入这个文件`security/ir.model.access.csv`  
```csv
 id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
 access_todo_task_group_user,todo.task.user,model_todo_task,base.group_user,1,1,1,1
```
### 行级别的访问控制
`ir.rule`
需要在data中加入这个文件`security/todo_access_rules.xml`  
```xml
<?xml version="1.0" encoding="utf-8"?>
<openerp>
    <data noupdate="1">
        <record id="todo_task_user_rule" model="ir.rule">
            <field name="name">Todo Task only for owner</field>
            <field name="model_id" ref="model_todo_task"/>
            <field name="domain_force">[('create_uid','=','user.id')]</field>
            <field name="groups" eval="[(4,ref('base.group_user'))]"/>
        </record>
    </data>
</openerp>
```  

## 继承和扩展<a id="1">
