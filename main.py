import kivy
kivy.require('2.1.0')
from kivymd.app import MDApp
# from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.tab import MDTabsBase,MDTabs
from kivymd.uix.navigationdrawer import MDNavigationLayout,MDNavigationDrawer
from kivy.uix.screenmanager import Screen,ScreenManager
from kivymd.uix.list import *
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import *
# from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.expansionpanel import MDExpansionPanel,MDExpansionPanelTwoLine, MDExpansionPanelOneLine
from kivymd.uix.textfield import MDTextField
from kivymd.uix.gridlayout import MDGridLayout
# from kivymd.uix.widget import MDWidget
from kivymd.uix.dialog import MDDialog
# from kivymd.font_definitions import theme_font_styles
from kivymd.uix.pickers import MDColorPicker,MDDatePicker,MDTimePicker
# from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
# import time
from kivymd.uix.selectioncontrol.selectioncontrol import MDCheckbox
from kivymd.uix.tooltip import MDTooltip
from kivymd.uix.progressbar import MDProgressBar
from kivy.metrics import dp
# from kivy.uix.image import Image
from kivymd.uix.snackbar import Snackbar
from database import *
from kivy.core.window import Window
from kivy.clock import Clock

Window.softinput_mode = 'below_target'


class TooltipMDIconButton(MDIconButton, MDTooltip):
    pass

class Tab(MDBoxLayout, MDTabsBase):
    def __init__(self,**kwargs):
        super(Tab,self).__init__(**kwargs)

class ToDo_box(MDBoxLayout):
    def __init__(self,title='',date='',time='',mode='new', **kwargs):
        super(ToDo_box, self).__init__(**kwargs)
        print(date)
        self.orientation='vertical'
        self.padding=dp(10)
        self.height = dp(280)
        self.spacing=dp(10)
        self.size_hint_y = None
        self.size_hint_x=0.3
        self.title=MDTextField(hint_text='ToDo title',text=title)
        self.add_widget(self.title)
        date_label=MDLabel(text='Due date',size_hint_y = None)
        time_label=MDLabel(text='Due time',size_hint_y = None)

        date_btn=MDIconButton(icon='calendar',on_release=self.open_date)
        time_btn=MDIconButton(icon='clock-time-eight-outline', on_release=self.open_time)

        self.date_layout=MDBoxLayout(orientation='horizontal',spacing=dp(10))
        self.time_layout=MDBoxLayout(orientation='horizontal',spacing=dp(10))

        self.date=date
        self.time=time

        self.add_widget(date_label)
        self.date_input=MDTextField(hint_text='DD-MM-YYYY',text='' if mode=='new' else self.date)
        self.date_layout.add_widget(self.date_input)
        self.date_layout.add_widget(date_btn)
        self.add_widget(self.date_layout)

        self.add_widget(time_label)
        self.time_input=MDTextField(hint_text='HH:MM:SS',text='' if mode=='new' else self.time)
        self.time_layout.add_widget(self.time_input)
        self.time_layout.add_widget(time_btn)
        self.add_widget(self.time_layout)

        if mode == 'new':
            self.date_picker = MDDatePicker()
        else:
            self.date_picker = MDDatePicker(day=int(date.split('-')[0]),
                             month=int(date.split('-')[1]),
                             year=int(date.split('-')[2]))

        self.date_picker.bind(on_save=self.on_save_date)

        self.time_picker = MDTimePicker()
        if mode=='new':
            current_time = str(datetime.now().hour) + ':' + str(datetime.now().minute) + ":" + str(datetime.now().second)
            currn_time = datetime.strptime(current_time, '%H:%M:%S').time()

        else:
            current_time = self.time_input.text
            currn_time = datetime.strptime(current_time, '%H:%M:%S').time()
        self.time_picker.set_time(currn_time)
        self.time_picker.bind(on_save=self.on_save_time)


    def open_date(self,instance):
        self.date_picker.open()

    def open_time(self,instance):
        self.time_picker.open()

    def on_save_date(self,instance,value,*args):
        print(value)
        self.date=value.strftime("%d-%m-%Y")
        value=self.date
        self.date_input.text=str(value)
        self.date_picker.dismiss()

    def on_save_time(self,instance,value,*args):
        print(value)
        self.time = value
        self.time_input.text=str(value)
        self.time_picker.dismiss()

    def save(self):
        try:
            if self.title.text.strip()=='':
                return None
            else:
                print(f'saving {self.date_input.text}, {self.time_input.text}')
                self.date=datetime.strptime(self.date_input.text,"%d-%m-%Y")
                self.time = datetime.strptime(self.time_input.text, "%H:%M:%S")
                return self.title.text, self.date, self.time
        except ValueError:
            return 'valueerror'
        except Exception:
            return None

class reminder_box(MDBoxLayout):
    def __init__(self,title='',date='',time='',mode='new',cycle='', **kwargs):
        super(reminder_box, self).__init__(**kwargs)
        print(date)
        self.orientation='vertical'
        self.padding=dp(10)
        self.height = dp(400)
        self.spacing=dp(5)
        self.size_hint_y = None
        self.size_hint_x=0.3
        self.title=MDTextField(hint_text='Reminder title',text=title)
        self.add_widget(self.title)
        date_label=MDLabel(text='Date',size_hint_y = None,adaptive_height=True)
        time_label=MDLabel(text='Time',size_hint_y = None,adaptive_height=True)

        date_btn=MDIconButton(icon='calendar',on_release=self.open_date)
        time_btn=MDIconButton(icon='clock-time-eight-outline', on_release=self.open_time)

        self.date_layout=MDBoxLayout(orientation='horizontal',spacing=dp(10),adaptive_height=True)
        self.time_layout=MDBoxLayout(orientation='horizontal',spacing=dp(10),adaptive_height=True)

        self.date=date
        self.time=time

        self.add_widget(date_label)
        self.date_input=MDTextField(hint_text='DD-MM-YYYY',text='' if mode=='new' else self.date)
        self.date_layout.add_widget(self.date_input)
        self.date_layout.add_widget(date_btn)
        self.add_widget(self.date_layout)

        self.add_widget(time_label)
        self.time_input=MDTextField(hint_text='HH:MM:SS',text='' if mode=='new' else self.time)
        self.time_layout.add_widget(self.time_input)
        self.time_layout.add_widget(time_btn)
        self.add_widget(self.time_layout)

        if mode == 'new':
            self.date_picker = MDDatePicker()
        else:
            self.date_picker = MDDatePicker(day=int(date.split('-')[0]),
                             month=int(date.split('-')[1]),
                             year=int(date.split('-')[2]))

        self.date_picker.bind(on_save=self.on_save_date)

        self.time_picker = MDTimePicker()
        if mode=='new':
            current_time = str(datetime.now().hour) + ':' + str(datetime.now().minute) + ":" + str(datetime.now().second)
            currn_time = datetime.strptime(current_time, '%H:%M:%S').time()

        else:
            current_time = self.time_input.text
            currn_time = datetime.strptime(current_time, '%H:%M:%S').time()
        self.time_picker.set_time(currn_time)
        self.time_picker.bind(on_save=self.on_save_time)

        # check boxes


        self.remind_cycle=''
        self.box1 = MDCheckbox(size_hint=(.15, .2), group='group',
                               on_release=lambda x: self.pressed('only-once'))
        label1 = MDLabel(text='Only once', adaptive_height=True)
        layout1 = MDGridLayout(cols=2, adaptive_height=True)
        layout1.add_widget(label1)
        layout1.add_widget(self.box1)

        self.box2 = MDCheckbox(size_hint=(.15, .2), group='group', size=(dp(1), dp(1)),
                               on_release=lambda x: self.pressed('every-day'))
        label2 = MDLabel(text='Every day', adaptive_height=True)
        layout2 = MDGridLayout(cols=2, adaptive_height=True)
        layout2.add_widget(label2)
        layout2.add_widget(self.box2)

        self.box3 = MDCheckbox(size_hint=(.15, .2), group='group', size=(dp(1), dp(1)),
                               on_release=lambda x: self.pressed('every-week'))
        label3 = MDLabel(text='Every week', adaptive_height=True)
        layout3 = MDGridLayout(cols=2, adaptive_height=True)
        layout3.add_widget(label3)
        layout3.add_widget(self.box3)

        self.box4 = MDCheckbox(size_hint=(.15, .2), group='group', size=(dp(.1), dp(.2)),
                               on_release=lambda x: self.pressed('every-month'))
        label4 = MDLabel(text='Every month', adaptive_height=True)
        layout4 = MDGridLayout(cols=2, adaptive_height=True)
        layout4.add_widget(label4)
        layout4.add_widget(self.box4)

        self.box5 = MDCheckbox(size_hint=(.15, .2), group='group', size=(dp(1), dp(1)),
                               on_release=lambda x: self.pressed('every-year'))
        label5 = MDLabel(text='Every year', adaptive_height=True)
        layout5 = MDGridLayout(cols=2, adaptive_height=True)
        layout5.add_widget(label5)
        layout5.add_widget(self.box5)

        layout = MDGridLayout(cols=1, spacing=dp(5))
        layout.add_widget(MDLabel(text='Remind me on',adaptive_height=True,bold=True))
        layout.add_widget(layout1)
        layout.add_widget(layout2)
        layout.add_widget(layout3)
        layout.add_widget(layout4)
        layout.add_widget(layout5)
        total_layout = MDBoxLayout(orientation='vertical')
        total_layout.add_widget(layout)
        boxes = {'only-once':self.box1,
                 'every-day':self.box2,
                 'every-week':self.box3,
                 'every-month':self.box4,
                 'every-year':self.box5}

        # label_text=['only-once','every-day','every-week','every-month','every-year']

        if mode!='new':
            box=boxes[cycle]
            box.state='down'
            self.remind_cycle=cycle

        self.add_widget(total_layout)

    def open_date(self,instance):
        self.date_picker.open()

    def open_time(self,instance):
        self.time_picker.open()

    def on_save_date(self,instance,value,*args):
        print(value)
        self.date=value.strftime("%d-%m-%Y")
        value=self.date
        self.date_input.text=str(value)
        self.date_picker.dismiss()

    def on_save_time(self,instance,value,*args):
        print(value)
        self.time = value
        self.time_input.text=str(value)
        self.time_picker.dismiss()

    def pressed(self,data):
        self.remind_cycle=data


    def save(self):
        try:
            if self.title.text.strip()=='' or self.remind_cycle=='':
                return None
            else:
                print(f'saving {self.date_input.text}, {self.time_input.text}')
                self.date=datetime.strptime(self.date_input.text,"%d-%m-%Y")
                self.time = datetime.strptime(self.time_input.text, "%H:%M:%S")
                return self.title.text, self.date, self.time,self.remind_cycle
        except ValueError:
            return 'valueerror'
        except Exception:
            return None

class my_list_box(MDBoxLayout):
    def __init__(self,title='',amount='',date='',bill_cycle='',mode='new', **kwargs):
        super(my_list_box, self).__init__(**kwargs)

        self.orientation='vertical'
        self.padding=dp(10)
        self.height = dp(300)
        self.spacing=dp(10)
        self.size_hint_y = None
        self.size_hint_x=0.3
        self.title=MDTextField(hint_text='List title',text='' if mode=='new' else title)
        self.add_widget(self.title)
        self.amount = MDTextField(hint_text='Amount', text='' if mode=='new' else str(amount))
        self.add_widget(self.amount)
        self.bill_cycle=MDTextField(hint_text='Billing/purchase frequency (months)',text='' if mode=='new' else str(bill_cycle))
        self.add_widget(self.bill_cycle)

        date_btn = MDIconButton(icon='calendar', on_release=self.open_date)

        self.date_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10))


        self.date = date
        print(f"Date in my_list_box {self.date} and type is {type(self.date)}")
        self.date_input = MDTextField(hint_text='Purchase/billing date', text='' if mode == 'new' else self.date)
        self.date_layout.add_widget(self.date_input)
        self.date_layout.add_widget(date_btn)
        self.add_widget(self.date_layout)


        if mode == 'new':
            self.date_picker = MDDatePicker()
        else:
            self.date_picker = MDDatePicker(day=int(date.split('-')[0]),
                                            month=int(date.split('-')[1]),
                                            year=int(date.split('-')[2]))

        self.date_picker.bind(on_save=self.on_save_date)

    def open_date(self,instance):
        self.date_picker.open()

    def on_save_date(self,instance,value,*args):
        print(value)
        self.date=value.strftime("%d-%m-%Y")
        value=self.date
        self.date_input.text=str(value)
        self.date_picker.dismiss()

    def save(self):
        # try:
        if self.title.text.strip()=='' or self.amount.text.strip()=='' or self.bill_cycle.text.strip()=='':
            return None
        else:
            try:
                if self.amount.text.isdigit() and self.bill_cycle.text.isdigit():
                    if int(self.amount.text)==0 or int(self.bill_cycle.text)==0:
                        return 'inputerror'
                    self.date = datetime.strptime(self.date_input.text, "%d-%m-%Y")
                    return self.title.text, self.amount.text, self.bill_cycle.text,self.date
                else:
                    return 'inputerror'
            except ValueError:
                return 'valueerror'

class income_list_box(MDBoxLayout):
    def __init__(self,title='',amount='',date='',income_cycle='',mode='new', **kwargs):
        super(income_list_box, self).__init__(**kwargs)

        self.orientation='vertical'
        self.padding=dp(10)
        self.height = dp(300)
        self.spacing=dp(10)
        self.size_hint_y = None
        self.size_hint_x=0.3
        self.title=MDTextField(hint_text='Source name',text='' if mode=='new' else title)
        self.add_widget(self.title)
        self.amount = MDTextField(hint_text='Amount', text='' if mode=='new' else str(amount))
        self.add_widget(self.amount)
        self.income_cycle=MDTextField(hint_text='Income frequency (months)',text='' if mode=='new' else str(income_cycle))
        self.add_widget(self.income_cycle)

        date_btn = MDIconButton(icon='calendar', on_release=self.open_date)

        self.date_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10))

        self.date = date
        print(f"Date in income_list_box {self.date} and type is {type(self.date)}")

        self.date_input = MDTextField(hint_text='Income date', text='' if mode == 'new' else self.date)
        self.date_layout.add_widget(self.date_input)
        self.date_layout.add_widget(date_btn)
        self.add_widget(self.date_layout)

        if mode == 'new':
            self.date_picker = MDDatePicker()

        else:
            self.date_picker = MDDatePicker(day=int(date.split('-')[0]),
                                            month=int(date.split('-')[1]),
                                            year=int(date.split('-')[2]))

        self.date_picker.bind(on_save=self.on_save_date)

    def open_date(self, instance):
        self.date_picker.open()

    def on_save_date(self, instance, value, *args):
        print(value)
        self.date = value.strftime("%d-%m-%Y")
        value = self.date
        self.date_input.text = str(value)
        self.date_picker.dismiss()

    def save(self):
        if self.title.text.strip() == '' or self.amount.text.strip() == '' or self.income_cycle.text.strip() == '':
            return None
        else:
            try:
                if self.amount.text.isdigit() and self.income_cycle.text.isdigit():
                    if int(self.amount.text) == 0 or int(self.income_cycle.text) == 0:
                        return 'inputerror'
                    self.date = datetime.strptime(self.date_input.text, "%d-%m-%Y")
                    return self.title.text, self.amount.text, self.income_cycle.text, self.date
                else:
                    return 'inputerror'
            except ValueError:
                return 'valueerror'
            except Exception:
                print('error in save')

class loan_list_box(MDBoxLayout):
    def __init__(self,title='',amount='',date='',loan_cycle='',mode='new', **kwargs):
        super(loan_list_box, self).__init__(**kwargs)

        self.orientation='vertical'
        self.padding=dp(10)
        self.height = dp(300)
        self.spacing=dp(10)
        self.size_hint_y = None
        self.size_hint_x=0.3
        self.title=MDTextField(hint_text='Loan name',text='' if mode=='new' else title)
        self.add_widget(self.title)
        self.amount = MDTextField(hint_text='Amount', text='' if mode=='new' else str(amount))
        self.add_widget(self.amount)
        self.loan_cycle=MDTextField(hint_text='Billing frequency (months)',text='' if mode=='new' else str(loan_cycle))
        self.add_widget(self.loan_cycle)

        date_btn = MDIconButton(icon='calendar', on_release=self.open_date)

        self.date_layout = MDBoxLayout(orientation='horizontal', spacing=dp(10))

        self.date = date
        print(f"Date in loan_list_box {self.date} and type is {type(self.date)}")

        self.date_input = MDTextField(hint_text='Purchase/billing date', text='' if mode == 'new' else self.date)
        self.date_layout.add_widget(self.date_input)
        self.date_layout.add_widget(date_btn)
        self.add_widget(self.date_layout)

        if mode == 'new':
            self.date_picker = MDDatePicker()

        else:
            self.date_picker = MDDatePicker(day=int(date.split('-')[0]),
                                            month=int(date.split('-')[1]),
                                            year=int(date.split('-')[2]))

        self.date_picker.bind(on_save=self.on_save_date)

    def open_date(self, instance):
        self.date_picker.open()

    def on_save_date(self, instance, value, *args):
        print(value)
        self.date = value.strftime("%d-%m-%Y")
        value = self.date
        self.date_input.text = str(value)
        self.date_picker.dismiss()

    def save(self):
        # try:
        if self.title.text.strip() == '' or self.amount.text.strip() == '' or self.loan_cycle.text.strip() == '':
            return None
        else:
            try:
                if self.amount.text.isdigit() and self.loan_cycle.text.isdigit():
                    if int(self.amount.text) == 0 or int(self.loan_cycle.text) == 0:
                        return 'inputerror'
                    self.date = datetime.strptime(self.date_input.text, "%d-%m-%Y")
                    return self.title.text, self.amount.text, self.loan_cycle.text, self.date
                else:
                    return 'inputerror'
            except ValueError:
                return 'valueerror'
            except Exception:
                print('error in save')

class filter_menu(MDBoxLayout):
    def __init__(self, **kwargs):
        super(filter_menu, self).__init__(**kwargs)
        self.orientation='vertical'
        self.padding=dp(10)
        self.height = dp(110)
        self.spacing=dp(10)
        self.size_hint_y = None
        self.box1 = MDCheckbox(size_hint=(.15, .2), group='group',
                               on_release=lambda x: self.pressed('remove-filter'))
        label1 = MDLabel(text='Remove filter', adaptive_height=True)
        layout1 = MDGridLayout(cols=2, adaptive_height=True)
        layout1.add_widget(label1)
        layout1.add_widget(self.box1)

        self.box2 = MDCheckbox(size_hint=(.15, .2), group='group', size=(dp(1), dp(1)),
                               on_release=lambda x: self.pressed('this-month'))
        label2 = MDLabel(text='This month', adaptive_height=True)
        layout2 = MDGridLayout(cols=2, adaptive_height=True)
        layout2.add_widget(label2)
        layout2.add_widget(self.box2)

        self.box3 = MDCheckbox(size_hint=(.15, .2), group='group', size=(dp(1), dp(1)),
                               on_release=lambda x: self.pressed('next-month'))
        label3 = MDLabel(text='Next month', adaptive_height=True)
        layout3 = MDGridLayout(cols=2, adaptive_height=True)
        layout3.add_widget(label3)
        layout3.add_widget(self.box3)

        layout = MDGridLayout(cols=1, spacing=dp(5))
        layout.add_widget(layout1)
        layout.add_widget(layout2)
        layout.add_widget(layout3)
        self.add_widget(layout)
        self.data = ''

    def pressed(self,data):
        self.data=data

    def save(self):
        if self.data=='':
            return None
        return self.data

class Noteable(MDApp):
    def build(self):
        # Tab names
        self.theme_cls.primary_palette = "Teal"
        self.title='Noteable'
        self.headers = ['Notes','ToDo','Management','Remainder']
        self.icon="things/images/noteable_icon.ico"

        # FloatLayout initialization

        self.layout = MDFloatLayout(pos_hint={'top':1})
        # self.main_layout.add_widget(main_layout_holder)

        self.menu_parent_color=(148/255, 200/255, 122/255, 0.62)
        self.menu_child_color=(91/255, 151/255, 157/255, 0.69)


        # App Bar
        self.topbar = MDTopAppBar(title='Notes', pos_hint={'top': 1},
                                  left_action_items=[['menu', self.open_dashboard]])
        self.disabled=False
        self.defaults = {'opacity': self.topbar.opacity, 'height': self.topbar.height}


        # Screen creation in navigation layout
        self.nav_layout = MDNavigationLayout()
        self.screen_manager = ScreenManager()


        notes_content = Screen(name='Notes')
        todo_content = Screen(name='ToDo')
        management_content = Screen(name='Management')
        reminder_content = Screen(name='Reminder')
        settings_content = Screen(name='Settings')


        # adding all screens to screen manager
        self.screen_manager.add_widget(notes_content)
        self.screen_manager.add_widget(todo_content)
        self.screen_manager.add_widget(management_content)
        self.screen_manager.add_widget(reminder_content)
        self.screen_manager.add_widget(settings_content)



        # list for settings
        # self.settings_menu=
        self.nav_layout.add_widget(self.screen_manager)



        # Navigation drawer
        self.nav_drawer = MDNavigationDrawer()
        self.scroll = ScrollView(do_scroll_y=False)
        self.options = MDList()
        self.scroll.add_widget(self.options)

        notes_icon = IconLeftWidgetWithoutTouch(icon='note')
        todo_icon = IconLeftWidgetWithoutTouch(icon='calendar-today')
        management_icon = IconLeftWidgetWithoutTouch(icon='view-grid')
        reminder_icon = IconLeftWidgetWithoutTouch(icon='reminder')
        settings_icon = IconLeftWidgetWithoutTouch(icon='cog')

        self.notes = OneLineIconListItem(text='Notes',
                                         on_release=lambda x: self.change_screen('Notes'),
                                         md_bg_color=(1,1,0,.7),radius=dp(20),divider=None)

        self.todo = OneLineIconListItem(text='ToDo',on_release=lambda x: self.change_screen('ToDo'),radius=dp(20),divider=None)

        self.management = OneLineIconListItem(text='Management',
                                              on_release=lambda x: self.change_screen('Management'),radius=dp(20),divider=None)

        self.reminder = OneLineIconListItem(text='Reminder',
                                            on_release=lambda x: self.change_screen('Reminder'),radius=dp(20),divider=None)

        self.settings = OneLineIconListItem(text='Settings',
                                            on_release=lambda x: self.change_screen('Settings'),radius=dp(20),divider=None)





        self.notes.add_widget(notes_icon)
        self.todo.add_widget(todo_icon)
        self.management.add_widget(management_icon)
        self.reminder.add_widget(reminder_icon)
        self.settings.add_widget(settings_icon)


        self.options.add_widget(self.notes)
        self.options.add_widget(self.todo)
        self.options.add_widget(self.management)
        self.options.add_widget(self.reminder)
        self.options.add_widget(self.settings)

        self.nav_drawer.add_widget(self.scroll)

        # setting menu color
        self.change_btn_color('Notes')

        # previous page
        self.previous = ''

        # Settings page
        # screens of settings

        # notes_settings=Screen(name='Notes_settings')
        # todo_settings=Screen(name='ToDo_settings')
        # management_settings=Screen(name='Management_settings')
        # reminder_settings=Screen(name='Reminder_settings')
        report_bug=Screen(name='Report_bug')
        about=Screen(name='About')

        # top bars of settings' items
        # notes_bar = MDTopAppBar(title='Notes settings', left_action_items=[['arrow-left',lambda x:self.change_screen('Settings'),'Back']], pos_hint={'top': 1})
        #
        # todo_bar = MDTopAppBar(title='ToDo settings', left_action_items=[['arrow-left',lambda x:self.change_screen('Settings'),'Back']], pos_hint={'top': 1})
        #
        # management_bar = MDTopAppBar(title='Management settings', left_action_items=[['arrow-left',lambda x:self.change_screen('Settings'),'Back']], pos_hint={'top': 1})
        #
        # reminder_bar = MDTopAppBar(title='Reminder settings', left_action_items=[['arrow-left',lambda x:self.change_screen('Settings'),'Back']], pos_hint={'top': 1})

        report_bar = MDTopAppBar(title='Report Bug', left_action_items=[['arrow-left',lambda x:self.change_screen('Settings'),'Back']], pos_hint={'top': 1})

        about_bar = MDTopAppBar(title='About', left_action_items=[['arrow-left',lambda x:self.change_screen('Settings'),'Back']], pos_hint={'top': 1})

        # notes_settings.add_widget(notes_bar)
        # todo_settings.add_widget(todo_bar)
        # management_settings.add_widget(management_bar)
        # reminder_settings.add_widget(reminder_bar)

        # report bug page content
        report_bug.add_widget(report_bar)
        report_layout=MDBoxLayout(orientation='vertical',pos=(dp(0),dp(-55)))
        report_info_layout=MDBoxLayout(orientation='vertical',padding=10,size_hint=(1,.2))
        report_temp_layout=MDBoxLayout()
        report_info=MDLabel(text='If you found any bug please report that to <email> with proper screenshot if possible.')
        report_info_layout.add_widget(report_info)
        report_layout.add_widget(report_info_layout)
        report_layout.add_widget(report_temp_layout)
        report_bug.add_widget(report_layout)

        # about page content
        about.add_widget(about_bar)
        about_layout = MDBoxLayout(orientation='vertical', pos=(dp(0), dp(-55)))
        about_info_layout = MDBoxLayout(orientation='vertical', padding=dp(10), size_hint=(1, .2))
        about_temp_layout = MDBoxLayout()
        about_info = MDLabel(
            text='Developer name : Jefi Ryan')
        about_info_layout.add_widget(about_info)
        about_layout.add_widget(about_info_layout)
        about_layout.add_widget(about_temp_layout)
        about.add_widget(about_layout)


        # labels of settings
        # notes_settings.add_widget(MDLabel(text='notes settings', halign='center'))
        # todo_settings.add_widget(MDLabel(text='todo settings', halign='center'))
        # management_settings.add_widget(MDLabel(text='management settings', halign='center'))
        # reminder_settings.add_widget(MDLabel(text='reminder settings', halign='center'))
        # appearance_settings.add_widget(MDLabel(text='appearance settings', halign='center'))
        # about.add_widget(MDLabel(text='about page', halign='center'))

        # Adding screens to screen manager
        # self.screen_manager.add_widget(notes_settings)
        # self.screen_manager.add_widget(todo_settings)
        # self.screen_manager.add_widget(management_settings)
        # self.screen_manager.add_widget(reminder_settings)
        self.screen_manager.add_widget(report_bug)
        self.screen_manager.add_widget(about)


        # items of settings page
        self.settings_list=MDList()
        scroll_settings=ScrollView(pos=(dp(0),dp(-55)))
        settings_layout=MDFloatLayout()
        settings_item_layout=MDBoxLayout(orientation='vertical',size_hint_y=None,adaptive_height=True)

        # notes_icon=IconLeftWidgetWithoutTouch(icon='note')
        # todo_icon=IconLeftWidgetWithoutTouch(icon='calendar-today')
        # management_icon=IconLeftWidgetWithoutTouch(icon='view-grid')
        # reminder_icon=IconLeftWidgetWithoutTouch(icon='reminder')
        color_icon=IconLeftWidgetWithoutTouch(icon='invert-colors')
        report_icon=IconLeftWidgetWithoutTouch(icon='bug')
        about_icon=IconLeftWidgetWithoutTouch(icon='information')

        # notes_settings_label=OneLineIconListItem(text='Notes settings',on_release=lambda x:self.change_screen('Notes_settings'))
        # todo_settings_label=OneLineIconListItem(text='ToDo settings',on_release=lambda x:self.change_screen('ToDo_settings'))
        # management_settings_label=OneLineIconListItem(text='Management settings',on_release=lambda x:self.change_screen('Management_settings'))
        # reminder_settings_label=OneLineIconListItem(text='Reminder settings',on_release=lambda x:self.change_screen('Reminder_settings'))
        color_menu=OneLineAvatarIconListItem(text='Dark mode',on_release=lambda x:x)
        report_bug_label=OneLineIconListItem(text='Report bug',on_release=lambda x:self.change_screen('Report_bug'))
        about_label=OneLineIconListItem(text='About',on_release=lambda x:self.change_screen('About'))

        # notes_settings_label.add_widget(notes_icon)
        # todo_settings_label.add_widget(todo_icon)
        # management_settings_label.add_widget(management_icon)
        # reminder_settings_label.add_widget(reminder_icon)
        self.switch_theme_icon=IconRightWidgetWithoutTouch(icon='toggle-switch-off-outline',on_release=self.change_app_theme)
        color_menu.add_widget(color_icon)
        color_menu.add_widget(self.switch_theme_icon)
        report_bug_label.add_widget(report_icon)
        about_label.add_widget(about_icon)

        # settings_item_layout.add_widget(notes_settings_label)
        # settings_item_layout.add_widget(todo_settings_label)
        # settings_item_layout.add_widget(management_settings_label)
        # settings_item_layout.add_widget(reminder_settings_label)
        settings_item_layout.add_widget(color_menu)
        settings_item_layout.add_widget(report_bug_label)
        settings_item_layout.add_widget(about_label)


        # Top bar of settings page
        self.settings_bar=MDTopAppBar(title='Settings',left_action_items=[['arrow-left',lambda x:self.change_screen('auto'),'Back']],pos_hint={'top':1})

        scroll_settings.add_widget(settings_item_layout)
        settings_layout.add_widget(self.settings_bar)
        settings_layout.add_widget(scroll_settings)
        # scroll_settings.add_widget(settings_layout)
        settings_content.add_widget(settings_layout)



        print('Available screens :', self.screen_manager.screens)

        # Notes app

        # list to show titles of notes

        self.search = False
        self.notes_layout = MDBoxLayout(orientation='vertical',pos=(dp(0),dp(-55)),spacing=dp(15),padding=dp(20))
        self.notes_header_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, size_hint=(1, .15),
                                               spacing=dp(20))
        self.notes_search_icon_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, adaptive_width=True)
        self.notes_search_icon = MDIconButton(icon='magnify', on_release=self.search_icon) # search note icon
        self.notes_create_icon = MDIconButton(icon='plus',on_release=lambda x:self.create_note(None,'New_note')) # create note icon

        # adding screen for creating new note
        self.new_note=Screen(name='New_note')
        self.screen_manager.add_widget(self.new_note)

        # content of new note page
        self.new_note_layout=MDBoxLayout(orientation='vertical',padding=(dp(20),dp(5),dp(20),dp(70)),spacing=dp(10),pos=(dp(0),dp(-55)))

        self.new_note_bar=MDTopAppBar(title='New Note',
                    left_action_items=[['arrow-left', lambda x: self.change_screen('Notes'), 'Back']],
                    pos_hint={'top': 1})

        self.new_note.add_widget(self.new_note_bar)

        note_sub_layout=MDGridLayout(cols=1,spacing=dp(10),adaptive_height=True)
        self.new_title_icon_layout = MDGridLayout(cols=2, spacing=dp(5), adaptive_height=True)
        self.new_note_icon_layout = MDBoxLayout(orientation='horizontal', size_hint=(.3, 0.1), adaptive_width=True,
                                                adaptive_height=True)
        self.note_new_title = MDLabel(text='New note', size_hint_y=None, size_hint_x=0.7, adaptive_height=True, font_size=dp(25),
                                      bold=True, font_style='H5')
        self.color_data=[1,1,1,0]
        self.color_saved=False
        self.color_new_note = MDIconButton(icon='format-color-fill',on_release=self.color_picker_app)
        self.color_picker = MDColorPicker(size_hint=(.45,.85))
        self.new_title_icon_layout.add_widget(self.note_new_title)
        self.new_note_icon_layout.add_widget(self.color_new_note)
        self.new_title_icon_layout.add_widget(self.new_note_icon_layout)
        note_sub_layout.add_widget(self.new_title_icon_layout)

        self.note_title=MDTextField(hint_text='Note Title',mode='fill')
        self.note_content=MDTextField(hint_text='Note content',mode='fill',multiline=True,max_height=dp(300),background_color=(1,1,0,1),foreground_color=(0, 0, 0, 1),text_color=(0,0,0,1),color_mode='custom')

        # new_note_scroll.add_widget(note_content)
        note_sub_layout.add_widget(self.note_title)
        note_sub_layout.add_widget(self.note_content)
        self.new_note_layout.add_widget(note_sub_layout)
        # new_note_layout.add_widget(note_content_layout)

        new_note_buttons = MDBoxLayout(orientation='horizontal', spacing=dp(10),
                                       size_hint=(1, 0.1), adaptive_width=True, pos_hint={'center_x': 0.5})
        note_save_btn = MDRaisedButton(text='Save',on_release=lambda x:self.save_note(None,self.note_title.text,self.note_content.text,self.color_data))
        note_cancel_btn = MDRaisedButton(text='Cancel',on_release=lambda x:self.discard_note(None,self.note_title.text,self.note_content.text))
        new_note_buttons.add_widget(note_save_btn)
        new_note_buttons.add_widget(note_cancel_btn)
        self.new_note_layout.add_widget(new_note_buttons)
        self.new_note.add_widget(self.new_note_layout)


        # adding to screen to view note
        self.view_note = Screen(name='View_note')
        self.screen_manager.add_widget(self.view_note)
        self.view_note_layout=MDBoxLayout(orientation='vertical',pos=(dp(0),dp(-55)))
        self.view_note_content_layout=MDGridLayout(cols=1,spacing=dp(5),padding=dp(20),)
        self.view_note_icon_layout=MDBoxLayout(orientation='horizontal',size_hint=(.3,0.1),adaptive_width=True,adaptive_height=True)

        self.view_title_icon_layout=MDGridLayout(cols=2,spacing=dp(5),padding=dp(20),adaptive_height=True)
        self.note_read_title = MDLabel(text='',size_hint_y=None,size_hint_x=0.7,adaptive_height=True,font_size=dp(25),bold=True,text_color=(0,0,0,1),theme_text_color= "Custom",font_style='H5')
        self.note_read_content = MDLabel(text='',adaptive_height=True,size_hint_y=None)
        self.scroll_note_read_content = ScrollView()
        self.scroll_note_read_content.add_widget(self.note_read_content)
        self.view_note_bar = MDTopAppBar(title='',
                                         left_action_items=[
                                             ['arrow-left', lambda x: self.change_screen('Notes'), 'Back']],
                                         pos_hint={'top': 1})
        self.view_note.add_widget(self.view_note_bar)
        self.view_title_icon_layout.add_widget(self.note_read_title)
        self.edit_view_note = MDIconButton(icon='clipboard-edit-outline',on_release=lambda x:self.edit_note(None,self.view_note_bar.title,self.notes_data[self.view_note_bar.title][0],
                                                                                                            self.notes_data[self.view_note_bar.title][1]))
        self.old_note_title=''
        self.view_note_icon_layout.add_widget(self.edit_view_note)
        self.view_title_icon_layout.add_widget(self.view_note_icon_layout)
        self.view_note_content_layout.add_widget(self.view_title_icon_layout)
        self.view_note_content_layout.add_widget(self.scroll_note_read_content)
        self.view_note_layout.add_widget(self.view_note_content_layout)
        self.view_note.add_widget(self.view_note_layout)



        # notes header icons
        self.notes_search_icon_layout.add_widget(self.notes_create_icon)
        self.notes_search_icon_layout.add_widget(self.notes_search_icon)
        self.notes_header_layout.add_widget(self.notes_search_icon_layout)

        self.search_bar = MDTextField(mode='rectangle', opacity=0)
        self.notes_header_layout.add_widget(self.search_bar)

        self.refresh_note=MDIconButton(icon='close',on_release=self.close_note_search_and_refresh,opacity=0)
        self.refresh_note_touch=False
        self.notes_header_layout.add_widget(self.refresh_note)

        self.notes_layout.add_widget(self.notes_header_layout)
        self.view = ScrollView()
        self.notes_content_layout = MDBoxLayout(orientation='vertical', adaptive_height=True, padding=(dp(10),dp(10),dp(10),dp(50)), spacing=dp(10))
        self.view.add_widget(self.notes_content_layout)  # adding layout to scroll view
        self.notes_layout.add_widget(self.view)
        self.items=dict()  # stores all the items (titles of note) used for searching
        notes_content.add_widget(self.notes_layout)
        # self.notes_data={'Groceries list':['',''],
        #                  'Shopping list':['',''],
        #                  'Movies list':['',''],
        #                  'Maths important formulas':['',''],
        #                  'Important numbers':['',''],
        #                  'All birthdays date':['',''],
        #                  'Important':['',''],
        #                  'Python notes':['',''],
        #                  'Sunday schedule':['',''],
        #                  '2022 Tour Plan':['',''],
        #                  }

        self.db_notes=db_notes()  # connecting to notes database
        self.notes_data=self.db_notes.retrieve()
        self.empty_notes=False

        self.show_notes_title()          # displaying all titles of note

        # ToDo App

        # list to show titles of todos

        self.todo_search = False
        self.todo_layout = MDBoxLayout(orientation='vertical', pos=(dp(0), dp(-55)), spacing=dp(15), padding=dp(20))
        self.todo_header_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, size_hint=(1, .15),
                                               spacing=dp(20))
        self.todo_search_icon_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, adaptive_width=True)
        # search todo icon
        self.todo_search_icon_btn = MDIconButton(icon='magnify', on_release=self.todo_search_icon)
        # create todo icon
        self.todo_create_icon_btn = MDIconButton(icon='plus', on_release=lambda x: self.pop_todo(None,"New ToDo"))


        # ToDo header icons

        self.todo_search_icon_layout.add_widget(self.todo_create_icon_btn)
        self.todo_search_icon_layout.add_widget(self.todo_search_icon_btn)
        self.todo_header_layout.add_widget(self.todo_search_icon_layout)

        self.todo_search_bar = MDTextField(mode='rectangle', opacity=0)
        self.todo_header_layout.add_widget(self.todo_search_bar)

        self.refresh_todo = MDIconButton(icon='close', on_release=self.close_todo_search_and_refresh, opacity=0)
        self.refresh_todo_touch = False
        self.todo_header_layout.add_widget(self.refresh_todo)
        self.todo_done=0

        self.todo_layout.add_widget(self.todo_header_layout)
        self.todo_view = ScrollView()
        self.todo_content_layout = MDBoxLayout(orientation='vertical', adaptive_height=True, padding=(dp(10), dp(10), dp(10), dp(50)),
                                                spacing=dp(10))
        self.todo_view.add_widget(self.todo_content_layout)  # adding layout to scroll view
        self.todo_layout.add_widget(self.todo_view)
        self.todo_items = dict()  # stores all the items (titles of ToDo) used for searching
        todo_content.add_widget(self.todo_layout)

        self.db_todo=db_todo() # connecting to todo database
        self.todo_data = self.db_todo.retrieve()
        self.empty_todo = False

        # self.show_todo_title()  # displaying all titles of ToDo

        # Reminder App

        # list to show titles of reminders

        self.reminder_search = False
        self.reminder_layout = MDBoxLayout(orientation='vertical', pos=(dp(0), dp(-55)), spacing=dp(15), padding=dp(20))
        self.reminder_header_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, size_hint=(1,.15),
                                              spacing=dp(20))
        self.reminder_search_icon_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, adaptive_width=True)
        # search Reminder icon
        self.reminder_search_icon_btn = MDIconButton(icon='magnify', on_release=self.reminder_search_icon)
        # create Reminder icon
        self.reminder_create_icon_btn = MDIconButton(icon='plus', on_release=lambda x: self.pop_reminder(None, "New Reminder"))

        # Reminder header icons

        self.reminder_search_icon_layout.add_widget(self.reminder_create_icon_btn)
        self.reminder_search_icon_layout.add_widget(self.reminder_search_icon_btn)
        self.reminder_header_layout.add_widget(self.reminder_search_icon_layout)

        self.reminder_search_bar = MDTextField(mode='rectangle', opacity=0)
        self.reminder_header_layout.add_widget(self.reminder_search_bar)

        self.refresh_reminder = MDIconButton(icon='close', on_release=self.close_reminder_search_and_refresh, opacity=0)
        self.refresh_reminder_touch = False
        self.reminder_header_layout.add_widget(self.refresh_reminder)
        self.reminder_done = 0

        self.reminder_layout.add_widget(self.reminder_header_layout)
        self.reminder_view = ScrollView()
        self.reminder_content_layout = MDBoxLayout(orientation='vertical', adaptive_height=True, padding=(dp(10), dp(10), dp(10), dp(50)),
                                               spacing=dp(10))
        self.reminder_view.add_widget(self.reminder_content_layout)  # adding layout to scroll view
        self.reminder_layout.add_widget(self.reminder_view)
        self.reminder_items = dict()  # stores all the items (titles of Reminder) used for searching
        reminder_content.add_widget(self.reminder_layout)

        self.db_reminder=db_reminder() # connecting to reminder database
        self.reminder_data = self.db_reminder.retrieve()
        self.empty_reminder = False

        # self.show_reminder_title()  # displaying all titles of Reminder

        # Management App

        management_tabs = MDTabs(pos_hint={'top':1})


        # Income tab

        income_content = Screen(name='income')
        self.income_list_search = False
        self.income_list_layout = MDBoxLayout(orientation='vertical', pos=(dp(0), dp(-55)), spacing=dp(15), padding=dp(20))
        self.income_list_header_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True,
                                                         size_hint=(1, .15),
                                                         spacing=dp(20))
        self.income_list_search_icon_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True,
                                                              adaptive_width=True)
        # search income_list icon
        self.income_list_search_icon_btn = MDIconButton(icon='magnify', on_release=self.income_list_search_icon)
        # create income_list icon
        self.income_list_create_icon_btn = MDIconButton(icon='plus',
                                                            on_release=lambda x: self.pop_income_list(None,
                                                                                                          "New income"))

        # income_list header icons

        self.income_list_search_icon_layout.add_widget(self.income_list_create_icon_btn)
        self.income_list_search_icon_layout.add_widget(self.income_list_search_icon_btn)
        self.income_list_header_layout.add_widget(self.income_list_search_icon_layout)

        self.income_list_search_bar = MDTextField(mode='rectangle', opacity=0)
        self.income_list_header_layout.add_widget(self.income_list_search_bar)

        self.refresh_income_list = MDIconButton(icon='close',
                                                    on_release=self.close_income_list_search_and_refresh, opacity=0)
        self.refresh_income_list_touch = False
        self.income_list_header_layout.add_widget(self.refresh_income_list)
        self.income_list_done = 0

        self.income_list_layout.add_widget(self.income_list_header_layout)
        self.income_list_view = ScrollView()
        self.income_list_content_layout = MDBoxLayout(orientation='vertical', adaptive_height=True,
                                                          padding=(dp(10), dp(10), dp(10), dp(50)),
                                                          spacing=dp(10))
        self.income_list_view.add_widget(self.income_list_content_layout)  # adding layout to scroll view
        self.income_list_layout.add_widget(self.income_list_view)
        self.income_list_items = dict()  # stores all the items (titles of income_list) used for searching
        income_list_tab = Tab(icon='', title='Income')
        income_list_tab.add_widget(self.income_list_layout)

        self.db_income=db_income() # connecting to income database
        self.income_list_data = self.db_income.retrieve()
        self.empty_income_list = False



        # my list tab

        my_list_content = Screen(name='my_list')
        self.management_list_search = False
        self.management_list_layout = MDBoxLayout(orientation='vertical', pos=(dp(0), dp(-55)), spacing=dp(15), padding=dp(20))
        self.management_list_header_parent_layout= MDBoxLayout(orientation='vertical', adaptive_height=True,size_hint=(1,.25),
                                                  spacing=dp(5))
        self.management_list_header_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True, size_hint=(1, .15),
                                                  spacing=dp(15))
        self.management_list_search_icon_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True,
                                                       adaptive_width=True)
        # search management_list icon
        self.management_list_search_icon_btn = MDIconButton(icon='magnify', on_release=lambda x:self.management_list_search_icon(None,self.management_custom,self.custom_data))


        # create management_list icon
        self.management_list_create_icon_btn = MDIconButton(icon='plus',
                                                     on_release=lambda x: self.pop_management_list(None, "New list"))

        # management_list header icons

        self.management_list_search_icon_layout.add_widget(self.management_list_create_icon_btn)
        self.management_list_search_icon_layout.add_widget(self.management_list_search_icon_btn)
        self.management_list_header_layout.add_widget(self.management_list_search_icon_layout)


        self.management_list_search_bar = MDTextField(mode='rectangle', opacity=0)
        self.management_list_header_layout.add_widget(self.management_list_search_bar)

        self.refresh_management_list = MDIconButton(icon='close', on_release=self.close_management_list_search_and_refresh, opacity=0)
        self.refresh_management_list_touch = False
        self.management_list_header_layout.add_widget(self.refresh_management_list)
        self.management_list_done = 0

        self.management_list_header_parent_layout.add_widget(self.management_list_header_layout)
        self.management_list_layout.add_widget(self.management_list_header_parent_layout)
        self.management_list_view = ScrollView()
        self.management_list_content_layout = MDBoxLayout(orientation='vertical', adaptive_height=True,
                                                   padding=(dp(10), dp(10), dp(10), dp(50)),
                                                   spacing=dp(10))
        self.management_list_view.add_widget(self.management_list_content_layout)  # adding layout to scroll view
        self.management_list_layout.add_widget(self.management_list_view)
        data = {
            'Remove filter': 'filter-off',
            'This month': 'filter',
            'Next month': 'page-next',
        }

        self.management_filter_btn = MDIconButton(icon='filter-outline',on_release=lambda x:self.pop_filter(self.management_list_data,self.show_management_list_title,self.management_filter_btn))
        self.management_list_header_parent_layout.add_widget(self.management_filter_btn)

        self.management_list_items = dict()  # stores all the items (titles of management_list) used for searching
        my_list_tab = Tab(icon='', title='My list')
        my_list_tab.add_widget(self.management_list_layout)

        self.db_management=db_my_list() # connecting to my list database
        self.management_list_data = self.db_management.retrieve()
        self.custom_data = ''
        self.management_custom = False
        self.empty_management_list = False

        # loan list tab

        loan_list_content = Screen(name='loan_list')
        self.loan_list_search = False
        self.loan_list_layout = MDBoxLayout(orientation='vertical', pos=(dp(0), dp(-55)), spacing=dp(15), padding=dp(20))
        self.loan_list_header_parent_layout = MDBoxLayout(orientation='vertical', adaptive_height=True,
                                                                size_hint=(1, .25),
                                                                spacing=dp(5))
        self.loan_list_header_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True,
                                                         size_hint=(1, .15),
                                                         spacing=dp(20))
        self.loan_list_search_icon_layout = MDBoxLayout(orientation='horizontal', adaptive_height=True,
                                                              adaptive_width=True)
        # search loan_list icon
        self.loan_list_search_icon_btn = MDIconButton(icon='magnify', on_release=lambda x: self.loan_list_search_icon(None,self.loan_custom,self.loan_custom_data))
        # create loan_list icon
        self.loan_list_create_icon_btn = MDIconButton(icon='plus',
                                                            on_release=lambda x: self.pop_loan_list(None,
                                                                                                          "New loan"))

        # loan_list header icons

        self.loan_list_search_icon_layout.add_widget(self.loan_list_create_icon_btn)
        self.loan_list_search_icon_layout.add_widget(self.loan_list_search_icon_btn)
        self.loan_list_header_layout.add_widget(self.loan_list_search_icon_layout)

        self.loan_list_search_bar = MDTextField(mode='rectangle', opacity=0)
        self.loan_list_header_layout.add_widget(self.loan_list_search_bar)

        self.refresh_loan_list = MDIconButton(icon='close',
                                                    on_release=self.close_loan_list_search_and_refresh, opacity=0)
        self.refresh_loan_list_touch = False
        self.loan_list_header_layout.add_widget(self.refresh_loan_list)
        self.loan_list_done = 0

        self.loan_list_header_parent_layout.add_widget(self.loan_list_header_layout)
        self.loan_list_layout.add_widget(self.loan_list_header_parent_layout)
        self.loan_list_view = ScrollView()
        self.loan_list_content_layout = MDBoxLayout(orientation='vertical', adaptive_height=True,
                                                          padding=(dp(10), dp(10), dp(10), dp(50)),
                                                          spacing=dp(10))
        self.loan_list_view.add_widget(self.loan_list_content_layout)  # adding layout to scroll view
        self.loan_list_layout.add_widget(self.loan_list_view)

        self.loan_filter_btn = MDIconButton(icon='filter-outline',
                                                  on_release=lambda x: self.pop_filter_loan(self.loan_list_data,
                                                                                       self.show_loan_list_title,self.loan_filter_btn))

        self.loan_list_header_parent_layout.add_widget(self.loan_filter_btn)
        self.loan_list_items = dict()  # stores all the items (titles of management_list) used for searching
        loan_list_tab = Tab(icon='', title='Loans')
        loan_list_tab.add_widget(self.loan_list_layout)

        self.db_loan=db_loan() # connecting to loan database
        self.loan_list_data = self.db_loan.retrieve()
        self.loan_custom_data = ''
        self.loan_custom = False
        self.empty_loan_list = False


        # Overview tab

        self.management_holder_layout = MDBoxLayout(orientation='vertical',pos=(dp(0), dp(-55)))
        overview_content = Screen(name='overview')
        col_1_color=(177/255, 76/255, 40/255, 0.62)
        col_2_color=(177/255, 76/255, 40/255, 0.62)


        overview_layout = MDBoxLayout(orientation='vertical',adaptive_height=True,spacing=dp(10),padding=(dp(10), dp(120), dp(10), dp(100)))

        # current income and amount of outcome

        self.current_info_layout=MDBoxLayout(spacing=dp(10),adaptive_height=True,size=(dp(400),dp(100)))

        self.current_income_layout=MDFloatLayout(radius=dp(10),md_bg_color=col_1_color)
        self.current_income=MDLabel(text='0',adaptive_height=True,font_style='H4',bold=True,pos_hint={'top':.8,'x':.03})
        self.current_income_label=MDLabel(text='Current Income\n',adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.current_income_layout.add_widget(self.current_income)
        self.current_income_layout.add_widget(self.current_income_label)

        self.current_expense_layout=MDFloatLayout(radius=dp(10),md_bg_color=col_2_color)
        self.current_expense = MDLabel(text='0',adaptive_height=True,font_style='H4',bold=True,pos_hint={'top':.8,'x':.03})
        self.current_expense_label = MDLabel(text='Current Expense\n',adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.current_expense_layout.add_widget(self.current_expense)
        self.current_expense_layout.add_widget(self.current_expense_label)

        self.current_info_layout.add_widget(self.current_income_layout)
        self.current_info_layout.add_widget(self.current_expense_layout)

        # total income sources and total expense sources

        self.total_layout = MDBoxLayout(spacing=dp(10),adaptive_height=True,size=(dp(400),dp(100)))
        self.total_incomes_layout = MDFloatLayout(radius=dp(10) ,md_bg_color=col_1_color)
        self.total_incomes = MDLabel(text='0', adaptive_height=True, font_style='H4', bold=True,pos_hint={'top':.8,'x':.03})
        self.total_incomes_label = MDLabel(text='Total Incomes\n', adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.total_incomes_layout.add_widget(self.total_incomes)
        self.total_incomes_layout.add_widget(self.total_incomes_label)

        self.total_expenses_layout = MDFloatLayout(radius=dp(10), md_bg_color=col_2_color)
        self.total_expenses = MDLabel(text='0', adaptive_height=True, font_style='H4', bold=True,pos_hint={'top':.8,'x':.03})
        self.total_expenses_label = MDLabel(text='Total Expenses\n', adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.total_expenses_layout.add_widget(self.total_expenses)
        self.total_expenses_layout.add_widget(self.total_expenses_label)

        self.total_layout.add_widget(self.total_incomes_layout)
        self.total_layout.add_widget(self.total_expenses_layout)

        # total loan and my list

        self.total_loan_my_list_layout = MDBoxLayout(spacing=dp(10), adaptive_height=True,size=(dp(400),dp(100)))
        self.total_loans_layout = MDFloatLayout(radius=dp(10), md_bg_color=col_1_color)
        self.total_loans = MDLabel(text='0', adaptive_height=True, font_style='H4',
                                     bold=True,pos_hint={'top':.8,'x':.03})
        self.total_loans_label = MDLabel(text='Total Loans\n', adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.total_loans_layout.add_widget(self.total_loans)
        self.total_loans_layout.add_widget(self.total_loans_label)

        self.total_my_list_layout = MDFloatLayout(radius=dp(10), md_bg_color=col_2_color)
        self.total_my_list = MDLabel(text='0', adaptive_height=True, font_style='H4',
                                      bold=True,pos_hint={'top':.8,'x':.03})
        self.total_my_list_label = MDLabel(text='Total My List\n', adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.total_my_list_layout.add_widget(self.total_my_list)
        self.total_my_list_layout.add_widget(self.total_my_list_label)

        self.total_loan_my_list_layout.add_widget(self.total_loans_layout)
        self.total_loan_my_list_layout.add_widget(self.total_my_list_layout)

        # current loan and next loan

        self.current_loan_next_loan_layout = MDBoxLayout(spacing=dp(10), adaptive_height=True,size=(dp(400),dp(100)))
        self.current_loans_layout = MDFloatLayout(radius=dp(10), md_bg_color=col_1_color)
        self.current_loans = MDLabel(text='0', adaptive_height=True, font_style='H4',
                                   bold=True,pos_hint={'top':.8,'x':.03})
        self.current_loans_label = MDLabel(text='Current month loan\n', adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.current_loans_layout.add_widget(self.current_loans)
        self.current_loans_layout.add_widget(self.current_loans_label)

        self.next_loan_layout = MDFloatLayout(radius=dp(10), md_bg_color=col_2_color)
        self.next_loan = MDLabel(text='0', adaptive_height=True, font_style='H4',
                                     bold=True,pos_hint={'top':.8,'x':.03})
        self.next_loan_label = MDLabel(text='Upcoming loan\n', adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.next_loan_layout.add_widget(self.next_loan)
        self.next_loan_layout.add_widget(self.next_loan_label)

        self.current_loan_next_loan_layout.add_widget(self.current_loans_layout)
        self.current_loan_next_loan_layout.add_widget(self.next_loan_layout)

        # current my list and next my list

        self.current_next_my_list_layout = MDBoxLayout(spacing=dp(10), adaptive_height=True,size=(dp(400),dp(100)))
        self.current_my_list_layout = MDFloatLayout(radius=dp(10), md_bg_color=col_1_color)
        self.current_my_list = MDLabel(text='0', adaptive_height=True, font_style='H4',
                                     bold=True,pos_hint={'top':.8,'x':.03})
        self.current_my_list_label = MDLabel(text='Current my list\n', adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.current_my_list_layout.add_widget(self.current_my_list)
        self.current_my_list_layout.add_widget(self.current_my_list_label)

        self.next_my_list_layout = MDFloatLayout(radius=dp(10),md_bg_color=col_2_color)
        self.next_my_list = MDLabel(text='0', adaptive_height=True, font_style='H4',
                                 bold=True,pos_hint={'top':.8,'x':.03})
        self.next_my_list_label = MDLabel(text='Upcoming my list\n', adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.next_my_list_layout.add_widget(self.next_my_list)
        self.next_my_list_layout.add_widget(self.next_my_list_label)

        self.current_next_my_list_layout.add_widget(self.current_my_list_layout)
        self.current_next_my_list_layout.add_widget(self.next_my_list_layout)

        # Income Percent and Savings

        self.total_percent_savings_layout = MDBoxLayout(spacing=dp(10), adaptive_height=True,size=(dp(400),dp(100)))
        self.total_percent_layout = MDFloatLayout(radius=dp(10),md_bg_color=(20/255, 214/255, 94/255, 0.8))
        self.total_percent = MDLabel(text='0.00 %', adaptive_height=True, font_style='H4',
                                   bold=True,pos_hint={'top':.8,'x':.03})
        self.total_percent_label = MDLabel(text='Spend Percentage', adaptive_height=True,font_style='Body2',pos_hint={'top':.25,'x':.03})
        self.total_percent_status = MDLabel(text='Excellent', adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.total_percent_layout.add_widget(self.total_percent)
        self.total_percent_layout.add_widget(self.total_percent_status)
        self.total_percent_layout.add_widget(self.total_percent_label)

        self.total_savings_layout = MDFloatLayout(radius=dp(10),md_bg_color=(0.8, 0.8, 0, 1))
        self.total_savings = MDLabel(text='0', adaptive_height=True, font_style='H4',bold=True,pos_hint={'top':.8,'x':.03})
        self.total_savings_label = MDLabel(text='Savings\n', adaptive_height=True,font_style='Body2',pos_hint={'top':.4,'x':.03})
        self.total_savings_layout.add_widget(self.total_savings)
        self.total_savings_layout.add_widget(self.total_savings_label)

        self.total_percent_savings_layout.add_widget(self.total_percent_layout)
        self.total_percent_savings_layout.add_widget(self.total_savings_layout)


        # management progress status
        self.top_temp=MDBoxLayout(adaptive_height=True)
        self.top_label=MDLabel(text=' ',adaptive_height=True)
        self.top_temp.add_widget(self.top_label)

        self.bottom_temp = MDBoxLayout(adaptive_height=True)
        self.bottom_label = MDLabel(text=' ', adaptive_height=True)
        self.bottom_temp.add_widget(self.bottom_label)

        self.parent_progress_layout=MDBoxLayout(adaptive_height=True)
        self.progress_layout=MDBoxLayout()
        self.total_progress_layout = MDBoxLayout(orientation='vertical',spacing=dp(30))

        savings_label=MDLabel(text='Savings')
        savings_progress_layout=MDBoxLayout(spacing=dp(5))
        self.savings_progress = MDProgressBar(value=0, size_hint_y=None, height=dp(10),color=(47/255, 234/255, 64/255, 0.8))
        self.savings_progress_percent=MDLabel(text='0.00 %')
        savings_progress_layout.add_widget(self.savings_progress)
        savings_progress_layout.add_widget(self.savings_progress_percent)

        my_list_label = MDLabel(text='My list')
        my_list_progress_layout = MDBoxLayout(spacing=dp(5))
        self.my_list_progress = MDProgressBar(value=0, size_hint_y=None, height=dp(10), color=(255/255, 223/255, 55/255, 0.8))
        self.my_list_progress_percent=MDLabel(text='0.00 %')
        my_list_progress_layout.add_widget(self.my_list_progress)
        my_list_progress_layout.add_widget(self.my_list_progress_percent)

        loans_label = MDLabel(text='Loans')
        loans_progress_layout = MDBoxLayout(spacing=dp(5))
        self.loans_progress = MDProgressBar(value=0, size_hint_y=None, height=dp(10), color=(237/255, 4/255, 42/255, 0.8))
        self.loans_progress_percent=MDLabel(text='0.00 %')
        loans_progress_layout.add_widget(self.loans_progress)
        loans_progress_layout.add_widget(self.loans_progress_percent)

        self.total_progress_layout.add_widget(savings_label)
        self.total_progress_layout.add_widget(savings_progress_layout)
        self.total_progress_layout.add_widget(my_list_label)
        self.total_progress_layout.add_widget(my_list_progress_layout)
        self.total_progress_layout.add_widget(loans_label)
        self.total_progress_layout.add_widget(loans_progress_layout)
        self.progress_layout.add_widget(self.total_progress_layout)

        self.parent_progress_layout.add_widget(self.progress_layout)



        overview_scroll=ScrollView(smooth_scroll_end=10)
        overview_layout.add_widget(self.top_temp)
        overview_layout.add_widget(self.parent_progress_layout)
        overview_layout.add_widget(self.bottom_temp)
        overview_layout.add_widget(self.total_percent_savings_layout)
        overview_layout.add_widget(self.current_info_layout)
        overview_layout.add_widget(self.current_loan_next_loan_layout)
        overview_layout.add_widget(self.current_next_my_list_layout)
        overview_layout.add_widget(self.total_layout)
        overview_layout.add_widget(self.total_loan_my_list_layout)



        overview_scroll.add_widget(overview_layout)
        overview_content.add_widget(overview_scroll)
        overview_tab = Tab(icon='', title='Overview')
        overview_tab.add_widget(overview_content)



        # adding all tabs to screen

        management_tabs.add_widget(overview_tab)
        management_tabs.add_widget(income_list_tab)
        management_tabs.add_widget(my_list_tab)
        management_tabs.add_widget(loan_list_tab)

        self.management_holder_layout.add_widget(management_tabs)
        management_content.add_widget(self.management_holder_layout)

        # putting everything sleep to wakeup when pressed
        self.todo_active=False
        self.management_active=False
        self.reminder_active=False

        self.update_total_income_expense()
        # self.show_management_list_title()  # displaying all titles of management_list
        # self.show_income_list_title()  # displaying all titles of income_list
        # self.show_loan_list_title()  # displaying all titles of loan_list

        # adding final layouts
        self.layout.add_widget(self.topbar)
        self.layout.add_widget(self.nav_layout)
        self.nav_drawer.set_state(new_state='close')
        self.layout.add_widget(self.nav_drawer)

        # screen history
        self.history_screen=[]

        # app theme
        self.theme=db_app()
        theme_style=self.theme.retrieve()[0][1]
        self.theme_cls.theme_style=theme_style
        self.change_app_theme(None,False)
        # self.change_app_theme(theme_style)

        # [['plus',self.create_note,'New note']]

        return self.layout

    def on_start(self):
        from kivy.base import EventLoop
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        if key == 27:
            # do what you want, return True for stopping the propagation
            if len(self.history_screen)>0:
                self.change_screen(self.history_screen.pop(),history=True)
                return True
            return False

    def change_app_theme(self,instance,switch=True):
        print('called')
        if switch==False:
            if self.theme_cls.theme_style == 'Light':
                self.switch_theme_icon.icon = 'toggle-switch-off-outline'

            else:
                self.switch_theme_icon.icon = 'toggle-switch'

        else:
            if self.theme_cls.theme_style=='Light':
                self.theme_cls.theme_style='Dark'
                self.theme.update('Dark')
                self.switch_theme_icon.icon='toggle-switch'

            else:
                self.theme_cls.theme_style='Light'
                self.theme.update('Light')
                self.switch_theme_icon.icon='toggle-switch-off-outline'

    def pop_filter(self, data,func,filter_icon):
        def save(instance,obj):

            self.pop_filter_list.dismiss()
            filter=obj.save()
            print(filter)
            results=dict()
            if filter=='this-month':
                self.management_custom = True
                filter_icon.icon = 'filter'
                for item in data:
                    if data[item][2].month == datetime.now().month and data[item][2].year==datetime.now().year:
                        results[item]=data[item]
                self.custom_data = results
                func(custom=True,data=results)

            elif filter=='next-month':
                self.management_custom = True
                filter_icon.icon='filter'
                for item in data:
                    if data[item][2].month == datetime.now().month+1 and data[item][2].year==datetime.now().year:
                        results[item]=data[item]
                self.custom_data = results
                func(custom=True, data=results)
            else:
                self.management_custom = False
                self.custom_data = data
                filter_icon.icon = 'filter-outline'
                func()


        def cancel(instance):
            self.pop_filter_list.dismiss()

        obj=filter_menu()
        self.pop_filter_list=MDDialog(
            title='Filter',
            type='custom',
            content_cls=obj,
            buttons=[
                MDRaisedButton(text='Apply', on_release=lambda x: save(None,obj)),
                MDRaisedButton(text='Cancel', on_release=cancel)
            ]
        )
        self.pop_filter_list.open()

    def pop_filter_loan(self, data,func,filter_icon):
        def save(instance,obj):

            self.pop_filter_list.dismiss()
            filter=obj.save()
            print(filter)
            results=dict()
            if filter=='this-month':
                self.loan_custom = True
                filter_icon.icon = 'filter'
                for item in data:
                    if data[item][2].month == datetime.now().month and data[item][2].year==datetime.now().year:
                        results[item]=data[item]
                self.loan_custom_data = results
                func(custom=True,data=results)

            elif filter=='next-month':
                self.loan_custom = True
                filter_icon.icon='filter'
                for item in data:
                    if data[item][2].month == datetime.now().month+1 and data[item][2].year==datetime.now().year:
                        results[item]=data[item]
                self.loan_custom_data = results
                func(custom=True, data=results)
            else:
                self.loan_custom = False
                self.loan_custom_data = data
                filter_icon.icon = 'filter-outline'
                func()


        def cancel(instance):
            self.pop_filter_list.dismiss()

        obj=filter_menu()
        self.pop_filter_list=MDDialog(
            title='Filter',
            type='custom',
            content_cls=obj,
            buttons=[
                MDRaisedButton(text='Apply', on_release=lambda x: save(None,obj)),
                MDRaisedButton(text='Cancel', on_release=cancel)
            ]
        )
        self.pop_filter_list.open()


    def update_total_income_expense(self):

        total_income_amount=0
        current_income_amount=0
        total_incomes_number=0
        current_incomes_number=0
        for source in self.income_list_data:
            income = self.income_list_data[source][0]
            total_income_amount += int(income)
            total_incomes_number += 1
            # income of this month
            if self.income_list_data[source][2].month == datetime.now().month and self.income_list_data[source][2].year == datetime.now().year:
                print(f'income source : {source}')
                current_income_amount += int(income)
                current_incomes_number += 1



        total_expense_amount=0
        current_expense_amount=0
        total_expenses_number=0
        total_loans_number=0
        current_loans_number=0
        total_my_list_number = 0
        current_my_list_number = 0
        next_my_list_number = 0
        next_loans_number = 0
        current_my_list_amount=0
        current_loans_amount=0

        for my_list in self.management_list_data:
            amount = self.management_list_data[my_list][0]
            total_expense_amount += int(amount)
            total_my_list_number += 1
            total_expenses_number += 1
            if self.management_list_data[my_list][2].month == datetime.now().month and self.management_list_data[my_list][2].year == datetime.now().year:
                current_expense_amount += int(amount)
                current_my_list_amount+= int(amount)
                current_my_list_number += 1

            elif self.management_list_data[my_list][2].month == datetime.now().month+1 and self.management_list_data[my_list][2].year == datetime.now().year:
                amount = self.management_list_data[my_list][0]
                next_my_list_number += 1

        for my_list in self.loan_list_data:
            amount = self.loan_list_data[my_list][0]
            total_expense_amount += int(amount)
            total_loans_number += 1
            if self.loan_list_data[my_list][2].month == datetime.now().month and self.loan_list_data[my_list][2].year == datetime.now().year:
                current_expense_amount += int(amount)
                current_loans_amount = int(amount)
                total_expenses_number += 1
                current_loans_number += 1

            elif self.loan_list_data[my_list][2].month == datetime.now().month+1 and self.loan_list_data[my_list][2].year == datetime.now().year:
                amount = self.loan_list_data[my_list][0]
                next_loans_number += 1

        income=total_income_amount
        if income>0:
            percent= (current_expense_amount/current_income_amount)*100

            if percent<50:
                status='Excellent'
                color=(20/255, 214/255, 94/255, 0.8)

            elif percent>50 and percent<70:
                status='Good'
                color=(26/255, 165/255, 237/255, 0.8)

            elif percent>70 and percent<90:
                status='Average'
                color=(237/255, 155/255, 26/255, 0.8)

            elif percent>90 and percent<95:
                status='Critical'
                color=(218/255, 39/255, 39/255, 0.8)

            else:
                status='Most Critical '
                color=(246/255, 11/255, 11/255, 0.8)

        else:
            percent=0.00
            status='No income'
            color=(20/255, 214/255, 94/255, 0.8)

        self.total_percent.text = "%.2f"%(percent) + ' %'
        self.total_percent_status.text = status
        self.total_percent_layout.md_bg_color = color

        savings = current_income_amount - current_expense_amount


        self.current_income.text = str(current_income_amount)
        # self.c_income.text = str(total_income_amount)
        self.total_incomes.text = str(total_incomes_number)
        self.total_savings.text=str(savings)
        self.current_expense.text = str(current_expense_amount)
        self.total_expenses.text = str(total_expenses_number)
        self.total_loans.text = str(total_loans_number)
        self.current_loans.text = str(current_loans_number)
        self.next_loan.text = str(next_loans_number)
        self.total_my_list.text = str(total_my_list_number)
        self.current_my_list.text = str(current_my_list_number)
        self.next_my_list.text = str(next_my_list_number)

        # updating progress bar
        if savings!=0 and current_income_amount!=0:
            self.savings_progress.value=(savings/current_income_amount)*100
            self.savings_progress_percent.text="%.2f"%((savings/current_income_amount)*100) + ' %'
        else:
            self.savings_progress.value = 0
            self.savings_progress_percent.text = "%.2f" % (0) + ' %'

        if current_my_list_amount!=0 and current_income_amount!=0:
            self.my_list_progress.value=(current_my_list_amount/current_income_amount)*100
            self.my_list_progress_percent.text="%.2f"%((current_my_list_amount/current_income_amount)*100) + ' %'
        else:
            self.my_list_progress.value = (0) * 100
            self.my_list_progress_percent.text = "%.2f" % (0) + ' %'

        if current_loans_amount!=0 and current_income_amount!=0:
            self.loans_progress.value=(current_loans_amount/current_income_amount)*100
            self.loans_progress_percent.text="%.2f"%((current_loans_amount/current_income_amount)*100) + ' %'
        else:
            self.loans_progress.value = (0) * 100
            self.loans_progress_percent.text = "%.2f" % (0) + ' %'

    def open_dashboard(self,instance):
        self.nav_drawer.set_state(new_state='toggle', animation=True)
        print(self.nav_drawer.state)

    def close_dashboard(self,instance):
        self.nav_drawer.set_state(new_state='close',animation=True)

    def change_btn_color(self,screen):
        screen_btn = {'Notes': self.notes, 'ToDo': self.todo, 'Management': self.management, 'Reminder': self.reminder,
                      'Settings': self.settings}
        note_screens = ['New_note', 'View_note']
        settings_screens = ['About','Report_bug']

        if screen!=self.screen_manager.current and screen in screen_btn and self.screen_manager.current in screen_btn:

            screen_btn[self.screen_manager.current].md_bg_color=(1,1,1,0)
            screen_btn[screen].md_bg_color=(1,1,0,.7)
            print(screen_btn[screen].text,(1,1,0,0.7))


        if self.screen_manager.current in note_screens and screen in screen_btn:
            screen_btn['Notes'].md_bg_color = (1, 1, 1, 0)
            screen_btn[screen].md_bg_color = (1, 1, 0, .7)
            print(screen_btn[screen].text, (1, 1, 0, 0.7))


        if self.screen_manager.current in settings_screens and screen in screen_btn:
            screen_btn['Settings'].md_bg_color = (1, 1, 1, 0)
            screen_btn[screen].md_bg_color = (1, 1, 0, .7)
            print(screen_btn[screen].text, (1, 1, 0, 0.7))


    def change_screen(self,name,history=False):

        screens_to_avoid = ['Settings', 'Notes_settings', 'ToDo_settings', 'Management_settings', 'Reminder_settings',
                            'Appearance_settings', 'About','Report_bug']
        screens=['Notes','ToDo','Management','Reminder']
        note_screens=['New_note','View_note']

        # adding screen history
        if history==False:
            if name == 'New_note':
                self.history_screen.append('Notes')
            else:
                self.history_screen.append(self.screen_manager.current)

        if name == 'ToDo' and self.todo_active==False:
            self.todo_active=True
            self.show_todo_title()

        if name == 'Management' and self.management_active==False:
            self.management_active=True
            self.show_income_list_title()
            self.show_management_list_title()
            self.show_loan_list_title()

        if name == 'Reminder' and self.reminder_active==False:
            self.reminder_active=True
            self.show_reminder_title()

        if name in screens:
            self.topbar.title=name
            print(f'screen to pass to color change {name}')
            self.change_btn_color(name)
            self.screen_manager.transition.direction = 'left'

        if self.screen_manager.current in screens and name == 'Settings':
            self.previous = self.screen_manager.current


        if name=='auto':
            if name == 'auto' and self.screen_manager.current == 'Settings':
                self.screen_manager.transition.direction = 'right'
                name=self.previous

                if name in screens:
                    print(name,'in auto')
                    self.change_btn_color(name)

        if self.screen_manager.current in note_screens:
            if name in screens or name == 'Settings':
                self.change_btn_color(name)
                self.screen_manager.transition.direction = 'left'

            if self.check_unsaved_notes():
                self.discard_note(None, self.note_title.text, self.note_content.text)
                return
            if self.screen_manager.current == 'View_note' and name == 'New_note':
                self.screen_manager.transition.direction = 'left'
            else:
                self.screen_manager.transition.direction = 'right'
        else:
            if name in note_screens and self.screen_manager.current=='Notes':
                self.screen_manager.transition.direction = 'left'

        if name in screens and self.screen_manager.current in note_screens:
            self.clear_note_cache()

        if name in screens_to_avoid:
            self.change_btn_color('Settings')
            if name=='Settings' and self.screen_manager.current in screens_to_avoid:
                self.screen_manager.transition.direction = 'right'
            else:
                self.screen_manager.transition.direction = 'left'

        self.screen_manager.current = name
        self.close_dashboard(None)

    def clear_note_cache(self):
        self.note_title.text=''
        self.note_content.text= ''


    def check_unsaved_notes(self):
        if self.note_title.text.strip()!='' and self.note_content.text.strip()!='':
            try:
                print('Now :',self.color_data)
                print('Previous :',self.notes_data[self.note_title.text][1])
                if self.note_content.text!=self.notes_data[self.note_title.text][0] or (self.color_data!=self.notes_data[self.note_title.text][1] and self.color_saved):
                    return True
                else:
                    return False
            except KeyError:
                return True
        else:
            return False

    def color_picker_app(self,instance):
        print('color picker called')
        self.color_picker.bind(on_select_color=self.select_color,on_release=self.get_color)
        self.color_picker.open()


    def select_color(self,instance,color_data):
        print(color_data)
        self.new_note_layout.md_bg_color= color_data
        print(self.note_content.text)



    def get_color(self,instance,type_color,color_data):
        self.color_data=color_data
        self.note_content.md_bg_color_mode = 'custom'
        self.note_content.md_bg_color = color_data
        self.color_data=color_data
        self.color_picker.dismiss()
        self.color_saved=True
        print(f"final color : {color_data}")

    def edit_note(self,instance,title,detail,color):
        print(title,detail)
        self.old_note_title=title
        self.note_title.text=title
        self.note_content.text=detail
        self.new_note_bar.title=title
        self.note_new_title.text=title
        self.new_note_layout.md_bg_color= color
        self.change_screen('New_note')


    def notes_view_del(self,name):
        # content of note list when pressed
        self.notes_sub_layout = MDBoxLayout(orientation='vertical', adaptive_height=True, adaptive_width=False,
                                            padding=(dp(0), dp(0), dp(30), dp(0)),
                                            md_bg_color=self.menu_child_color, radius=(dp(0), dp(0), dp(10), dp(10)))
        item = OneLineAvatarIconListItem(divider=None)
        view = IconRightWidget(icon='eye',on_release=lambda x:self.show_notes_page(None,name))
        delete = IconRightWidget(icon='delete',on_release=lambda x:self.delete_notes_page(None,name))
        item.add_widget(view)
        item.add_widget(delete)
        self.notes_sub_layout.add_widget(item)
        return self.notes_sub_layout

    def formal_date(self,date):
        month_data=['Jan','Feb','Mar','Apr','May',"June","July",'Aug',"Sep",'Oct',"Nov",'Dec']
        day,month,year=date.split('-')
        month=month_data[int(month)-1]
        month=str(month)
        if day==1:
            joiner='st'
        elif day==2:
            joiner='nd'
        elif day==3:
            joiner='rd'
        else:
            joiner='th'
        formal_data=day+joiner+' '+month+', '+year
        return formal_data

    def formal_day_month(self,date,mode='both'):
        month_data=['Jan','Feb','Mar','Apr','May',"June","July",'Aug',"Sep",'Oct',"Nov",'Dec']
        day,month,year=date.split('-')
        month = month_data[int(month) - 1]
        month = str(month)

        if day==1:
            joiner='st'
        elif day==2:
            joiner='nd'
        elif day==3:
            joiner='rd'
        else:
            joiner='th'

        if mode=='day':
            formal_data=day+joiner
        elif mode=='month':
            formal_data=month
        else:
            formal_data=day+joiner+' '+month
        return formal_data

    def formal_time(self,time):
        time=time.split(":")
        hour,minute,second=time
        if int(hour)>12:
            hour=str(abs(12-int(hour)))
            time_of_day='PM'
        elif int(hour)==12:
            time_of_day = 'PM'
        else:
            time_of_day='AM'
        formal_data=hour+':'+minute+" "+time_of_day
        return formal_data

    def todo_edit_del(self,name):

        layout=MDBoxLayout(orientation='vertical',spacing=dp(10),padding=(dp(10), dp(5), dp(10), dp(10)),md_bg_color=self.menu_child_color,
                           radius=(dp(0), dp(0), dp(10), dp(10)),adaptive_height=True)
        data_layout=MDBoxLayout(adaptive_height=True,orientation='vertical')
        date=self.date_extractor(self.todo_data[name][0])
        time=self.time_extractor(self.todo_data[name][1])

        #temp
        top_temp = MDBoxLayout(adaptive_height=True)
        top_label = MDLabel(text=' \n', adaptive_height=True)
        top_temp.add_widget(top_label)

        bottom_temp = MDBoxLayout(adaptive_height=True)
        bottom_label = MDLabel(text=' \n', adaptive_height=True)
        bottom_temp.add_widget(bottom_label)

        info = MDLabel(
            text='Due on '+self.formal_date(date) +' at '+self.formal_time(time)+'\n')
        data_layout.add_widget(top_temp)
        data_layout.add_widget(info)
        data_layout.add_widget(bottom_temp)

        self.todo_complete_btn=MDIconButton(icon='checkbox-marked-circle-outline', on_release=lambda x: self.todo_completed(None,name))
        view = MDIconButton(icon='clipboard-edit-outline',on_release=lambda x:self.pop_todo(None,name,'edit',self.todo_data[name][0],self.todo_data[name][1]))
        delete = MDIconButton(icon='delete',on_release=lambda x:self.delete_todo_page(None,name))

        temp_layout=MDBoxLayout()
        temp_layout.add_widget(MDLabel(text='',size_hint_y=None))
        icon_layout=MDBoxLayout(orientation='horizontal',spacing=dp(5),adaptive_height=True,adaptive_width=True)
        icon_layout.add_widget(self.todo_complete_btn)
        icon_layout.add_widget(view)
        icon_layout.add_widget(delete)

        # data_layout.add_widget(layout)

        layout.add_widget(data_layout)
        temp_layout.add_widget(icon_layout)
        layout.add_widget(temp_layout)

        return layout

    def reminder_edit_del(self,name):

        layout=MDBoxLayout(orientation='vertical',spacing=dp(10),padding=(dp(10), dp(5), dp(10), dp(10)),md_bg_color=self.menu_child_color,
                           radius=(dp(0), dp(0), dp(10), dp(10)),adaptive_height=True)
        data_layout=MDBoxLayout(adaptive_height=True,orientation='vertical')

        date=self.date_extractor(self.reminder_data[name][0])
        time=self.time_extractor(self.reminder_data[name][1])
        cycle=self.reminder_data[name][2]

        # temp
        top_temp = MDBoxLayout(adaptive_height=True)
        top_label = MDLabel(text=' \n', adaptive_height=True)
        top_temp.add_widget(top_label)

        bottom_temp = MDBoxLayout(adaptive_height=True)
        bottom_label = MDLabel(text=' \n', adaptive_height=True)
        bottom_temp.add_widget(bottom_label)

        if cycle=='only-once':
            info = MDLabel(
                text='On '+self.formal_date(date) +' at '+self.formal_time(time)+'\n',size_hint_y=None)
            data_layout.add_widget(top_temp)
            data_layout.add_widget(info)
            data_layout.add_widget(bottom_temp)

        elif cycle=='every-day':
            info = MDLabel(
                text='Every day at ' + self.formal_time(time)+'\n', size_hint_y=None)
            data_layout.add_widget(top_temp)
            data_layout.add_widget(info)
            data_layout.add_widget(bottom_temp)

        elif cycle=='every-week':
            week=['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
            week=week[self.reminder_data[name][0].weekday()]
            info = MDLabel(
                text="Every "+ week + ' at '+ self.formal_time(time)+'\n', size_hint_y=None)
            data_layout.add_widget(top_temp)
            data_layout.add_widget(info)
            data_layout.add_widget(bottom_temp)

        elif cycle=='every-month':
            info = MDLabel(
                text='Every month on ' + self.formal_day_month(date,mode='day')+ ' at '+ self.formal_time(time)+'\n', size_hint_y=None)
            data_layout.add_widget(top_temp)
            data_layout.add_widget(info)
            data_layout.add_widget(bottom_temp)

        elif cycle=='every-year':
            info = MDLabel(
                text='Every year on ' + self.formal_day_month(date)+ ' at '+ self.formal_time(time)+'\n', size_hint_y=None)
            data_layout.add_widget(top_temp)
            data_layout.add_widget(info)
            data_layout.add_widget(bottom_temp)


        view = MDIconButton(icon='clipboard-edit-outline',on_release=lambda x:self.pop_reminder(None,name,'edit',cycle,self.reminder_data[name][0],self.reminder_data[name][1]))
        delete = MDIconButton(icon='delete',on_release=lambda x:self.delete_reminder_page(None,name))

        temp_layout=MDBoxLayout()
        temp_layout.add_widget(MDLabel(text='',size_hint_y=None))
        icon_layout=MDBoxLayout(orientation='horizontal',spacing=5,adaptive_height=True,adaptive_width=True)
        icon_layout.add_widget(view)
        icon_layout.add_widget(delete)

        # data_layout.add_widget(layout)

        layout.add_widget(data_layout)
        temp_layout.add_widget(icon_layout)
        layout.add_widget(temp_layout)

        return layout

    def management_list_edit_del(self,name):

        layout=MDBoxLayout(orientation='vertical',spacing=dp(10),padding=(dp(10), dp(5), dp(10), dp(10)),md_bg_color=self.menu_child_color,
                           radius=(dp(0), dp(0), dp(10), dp(10)),adaptive_height=True)
        data_layout=MDBoxLayout(adaptive_height=True,orientation='vertical')
        amount=self.management_list_data[name][0]
        cycle=self.management_list_data[name][1]
        date=self.management_list_data[name][2]

        # temp
        top_temp = MDBoxLayout(adaptive_height=True)
        top_label = MDLabel(text=' \n', adaptive_height=True)
        top_temp.add_widget(top_label)

        bottom_temp = MDBoxLayout(adaptive_height=True)
        bottom_label = MDLabel(text=' \n', adaptive_height=True)
        bottom_temp.add_widget(bottom_label)

        if int(cycle)==1:
            self.management_info = MDLabel(
                text='Billing/purchasing every month \n'+'Next purchase or due date '+self.date_extractor(date)+'\n',size_hint_y=None)
        else:
            self.management_info = MDLabel(
                text='Billing/purchasing every ' + cycle + ' months\n'+'Next purchase or due date '+self.date_extractor(date)+'\n', size_hint_y=None)

        data_layout.add_widget(top_temp)
        data_layout.add_widget(self.management_info)
        data_layout.add_widget(bottom_temp)

        print(f"management custom : {self.management_custom}")
        complete = MDIconButton(icon='checkbox-marked-circle-outline',
                                              on_release=lambda x: self.purchase_completed(None, name,amount,cycle,self.management_list_data,self.db_management,self.show_management_list_title,
                                                                                           self.management_custom,self.custom_data))
        view = MDIconButton(icon='clipboard-edit-outline',on_release=lambda x:self.pop_management_list(None,name,amount,date,cycle,'edit'))
        delete = MDIconButton(icon='delete',on_release=lambda x:self.delete_management_list_page(None,name))

        temp_layout=MDBoxLayout()
        temp_layout.add_widget(MDLabel(text='',size_hint_y=None))
        icon_layout=MDBoxLayout(orientation='horizontal',spacing=5,adaptive_height=True,adaptive_width=True)
        icon_layout.add_widget(complete)
        icon_layout.add_widget(view)
        icon_layout.add_widget(delete)

        # data_layout.add_widget(layout)

        layout.add_widget(data_layout)
        temp_layout.add_widget(icon_layout)
        layout.add_widget(temp_layout)

        return layout

    def purchase_completed(self,instance,name,amount,cycle,dict_data,data,func,custom,content):

        temp_date=dict_data[name][2]+relativedelta(months=int(cycle))
        data.update(name,name, amount, cycle, temp_date)
        self.management_list_data = data.retrieve()
        self.update_total_income_expense()
        print(f"custom : {custom}")
        func(custom=custom,data=content)

    def loan_completed(self,instance,name,amount,cycle,dict_data,data,func,custom,content):
        temp_date=dict_data[name][2]+relativedelta(months=int(cycle))
        data.update(name,name, amount, cycle, temp_date)
        self.loan_list_data = data.retrieve()
        self.update_total_income_expense()
        print(f"custom : {custom}")
        func(custom=custom,data=content)

    def income_completed(self,instance,name,amount,cycle,dict_data,data,func):
        temp_date=dict_data[name][2]+relativedelta(months=int(cycle))
        data.update(name,name,amount, cycle, temp_date)
        self.income_list_data=data.retrieve()
        self.update_total_income_expense()
        func()


    def income_list_edit_del(self,name):

        layout=MDBoxLayout(orientation='vertical',spacing=dp(10),padding=(dp(10), dp(5), dp(10), dp(10)),md_bg_color=self.menu_child_color,
                           radius=(dp(0), dp(0), dp(10), dp(10)),adaptive_height=True)
        data_layout=MDBoxLayout(adaptive_height=True,orientation='vertical')
        amount = self.income_list_data[name][0]
        cycle = self.income_list_data[name][1]
        date = self.income_list_data[name][2]

        # temp
        top_temp = MDBoxLayout(adaptive_height=True)
        top_label = MDLabel(text=' \n', adaptive_height=True)
        top_temp.add_widget(top_label)

        bottom_temp = MDBoxLayout(adaptive_height=True)
        bottom_label = MDLabel(text=' \n', adaptive_height=True)
        bottom_temp.add_widget(bottom_label)

        upcoming_date = date + relativedelta(months=int(cycle))
        if int(cycle) == 1:
            info = MDLabel(
                text='Income every month\n'+ 'Next income date ' + self.date_extractor(upcoming_date)+'\n', size_hint_y=None)
        else:
            info = MDLabel(
                text='Income every ' + cycle + ' months\n' + 'Next due date ' + self.date_extractor(date)+'\n', size_hint_y=None)

        data_layout.add_widget(top_temp)
        data_layout.add_widget(info)
        data_layout.add_widget(bottom_temp)

        complete = MDIconButton(icon='checkbox-marked-circle-outline',
                                on_release=lambda x: self.income_completed(None, name, amount, cycle,
                                                                             self.income_list_data,
                                                                             self.db_income,
                                                                             self.show_income_list_title))
        view = MDIconButton(icon='clipboard-edit-outline',on_release=lambda x:self.pop_income_list(None,name,amount,date,cycle,'edit'))
        delete = MDIconButton(icon='delete',on_release=lambda x:self.delete_income_list_page(None,name))

        temp_layout=MDBoxLayout()
        temp_layout.add_widget(MDLabel(text='',size_hint_y=None))
        icon_layout=MDBoxLayout(orientation='horizontal',spacing=5,adaptive_height=True,adaptive_width=True)
        icon_layout.add_widget(complete)
        icon_layout.add_widget(view)
        icon_layout.add_widget(delete)

        # data_layout.add_widget(layout)

        layout.add_widget(data_layout)
        temp_layout.add_widget(icon_layout)
        layout.add_widget(temp_layout)

        return layout

    def loan_list_edit_del(self,name):

        layout=MDBoxLayout(orientation='vertical',spacing=dp(10),padding=(dp(10), dp(5), dp(10), dp(10)),md_bg_color=self.menu_child_color,
                           radius=(dp(0), dp(0), dp(10), dp(10)),adaptive_height=True)
        data_layout=MDBoxLayout(adaptive_height=True,orientation='vertical')
        amount = self.loan_list_data[name][0]
        cycle = self.loan_list_data[name][1]
        date = self.loan_list_data[name][2]
        # temp
        top_temp = MDBoxLayout(adaptive_height=True)
        top_label = MDLabel(text=' \n', adaptive_height=True)
        top_temp.add_widget(top_label)

        bottom_temp = MDBoxLayout(adaptive_height=True)
        bottom_label = MDLabel(text=' \n', adaptive_height=True)
        bottom_temp.add_widget(bottom_label)

        print(f"date in loan_list_del {date}")
        if int(cycle) == 1:
            self.loan_info = MDLabel(
                text='Billing every month \n' + 'Next due date ' + self.date_extractor(date)+'\n',
                size_hint_y=None)
        else:
            self.loan_info = MDLabel(
                text='Billing every ' + cycle + ' months\n' + 'Next due date ' + self.date_extractor(
                    date)+'\n', size_hint_y=None)

        data_layout.add_widget(top_temp)
        data_layout.add_widget(self.loan_info)
        data_layout.add_widget(bottom_temp)

        complete = MDIconButton(icon='checkbox-marked-circle-outline',
                                on_release=lambda x: self.loan_completed(None, name, amount, cycle,
                                                                             self.loan_list_data,
                                                                             self.db_loan,
                                                                             self.show_loan_list_title,
                                                                             self.loan_custom,self.loan_custom_data))
        view = MDIconButton(icon='clipboard-edit-outline',on_release=lambda x:self.pop_loan_list(None,name,amount,date,cycle,'edit'))
        delete = MDIconButton(icon='delete',on_release=lambda x:self.delete_loan_list_page(None,name))

        temp_layout=MDBoxLayout()
        temp_layout.add_widget(MDLabel(text='',size_hint_y=None))
        icon_layout=MDBoxLayout(orientation='horizontal',spacing=5,adaptive_height=True,adaptive_width=True)
        icon_layout.add_widget(complete)
        icon_layout.add_widget(view)
        icon_layout.add_widget(delete)

        # data_layout.add_widget(layout)

        layout.add_widget(data_layout)
        temp_layout.add_widget(icon_layout)
        layout.add_widget(temp_layout)

        return layout


    def todo_completed(self,instance,name):
        Snackbar(
            text="Congrats!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5,
            duration=1
        ).open()
        self.delete_todo_page(None,name)



    # def check_todo_complete_condition(self):
    #     print(self.todo_done)
    #     if self.todo_done==0:
    #         self.todo_complete_btn.opacity = 0


    def todo_mark_complete(self,instance):
        while len(self.todo_items)>0:
            for item in self.todo_items:
                if self.todo_data[item.panel_cls.text.strip()][2]=='complete':
                    print(f'found {item.panel_cls.text.strip()}')
                    self.todo_content_layout.remove_widget(item)
                    self.todo_items.remove(item)
                    self.db_todo.delete(item.panel_cls.text.strip())
                    self.todo_data = self.db_todo.retrieve()
                    print('deleted')
                    break

            self.todo_complete_btn.opacity = 0
            self.show_todo_title()


    def date_extractor(self,data):
        if not isinstance(data,str):
            data=str(data.day).zfill(2)+'-'+str(data.month).zfill(2)+'-'+str(data.year).zfill(2)
            print(data)
            return data

    def time_extractor(self,data):
        if not isinstance(data, str):
            data=str(data.hour).zfill(2)+':'+str(data.minute).zfill(2)+':'+str(data.second).zfill(2)
            print(data)
            return data

    def pop_todo(self,*args):
        Snackbar(
            text="Loading...!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5,
            duration=1
        ).open()

        Clock.schedule_once(lambda x: self.pop_todo_process(*args), .5)


    def pop_todo_process(self,instance,title,mode='new',date='',time=''):

        if mode=='new':
            obj=ToDo_box()
        elif mode=='edit':
            obj = ToDo_box(title,self.date_extractor(date),self.time_extractor(time),mode)
        self.todo_popup=MDDialog(
            title=title,
            type='custom',
            content_cls=obj,
            buttons=[
                MDRaisedButton(text='Save', on_release=lambda x: save(obj,title)),
                MDRaisedButton(text='Cancel', on_release=lambda x: cancel(obj))
            ]
        )


        self.todo_popup.open()
        def open(instance):
            self.todo_popup.open()

        Clock.schedule_once(open, 1)



        def save(obj,old_title):
            if obj.save() not in [None,'valueerror']:
                print(f"received {obj.save()}")
                if mode == 'new':
                    title, date, time = obj.save()
                    self.db_todo.insert(title, date, time, 'incomplete')
                    self.todo_data = self.db_todo.retrieve()
                    if 'empty' in self.todo_items:
                        item = self.todo_items['empty']
                        self.todo_content_layout.remove_widget(item)
                        self.todo_items.pop('empty')
                    if title in self.todo_items:
                        item = self.todo_items[title]
                        self.todo_content_layout.remove_widget(item)
                        self.todo_items.pop(title)
                    self.display_todo_title(title)


                elif mode == 'edit':
                    title, date, time = obj.save()
                    self.todo_data[title] = self.todo_data.pop(old_title)
                    self.db_todo.update(old_title, title, date, time, 'incomplete')
                    self.todo_data = self.db_todo.retrieve()
                    if 'empty' in self.todo_items:
                        item = self.todo_items['empty']
                        self.todo_content_layout.remove_widget(item)
                        self.todo_items.pop('empty')
                    if title in self.todo_items:
                        item = self.todo_items[title]
                        self.todo_content_layout.remove_widget(item)
                        self.todo_items.pop(title)
                    if old_title in self.todo_items:
                        item = self.todo_items[old_title]
                        self.todo_content_layout.remove_widget(item)
                        self.todo_items.pop(old_title)
                    self.display_todo_title(title)

                print(self.todo_data)
                self.todo_popup.dismiss()


            elif obj.save()==None:
                self.popup_err_msg_todo()

            elif obj.save()=='valueerror':
                self.popup_err_msg_todo('Invalid date or time!')


        def cancel(obj):
            self.todo_popup.dismiss()

    def pop_reminder(self,*args):
        Snackbar(
            text="Loading...!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5,
            duration=1
        ).open()

        Clock.schedule_once(lambda x: self.pop_reminder_process(*args), .5)

    def pop_reminder_process(self,instance,title,mode='new',cycle='',date='',time=''):

        Snackbar(
            text="Loading...!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5,
            duration=1
        ).open()

        if mode=='new':
            obj=reminder_box()
        elif mode=='edit':
            obj = reminder_box(title,self.date_extractor(date),self.time_extractor(time),mode,cycle)
        self.reminder_popup=MDDialog(
            title=title,
            type='custom',
            content_cls=obj,
            buttons=[
                MDRaisedButton(text='Save', on_release=lambda x: save(obj,title)),
                MDRaisedButton(text='Cancel', on_release=lambda x: cancel(obj))
            ]
        )



        def open(instance):
            self.reminder_popup.open()

        Clock.schedule_once(open, 1)


        def save(obj,old_title):
            if obj.save() not in [None,'valueerror']:
                print(f"received {obj.save()}")
                if mode == 'new':

                    title, date, time, cycle = obj.save()
                    self.db_reminder.insert(title, date, time, cycle)
                    self.reminder_data = self.db_reminder.retrieve()

                    if title in self.reminder_items:
                        item = self.reminder_items[title]
                        self.reminder_content_layout.remove_widget(item)
                        self.reminder_items.pop(title)

                    if 'empty' in self.reminder_items:
                        item = self.reminder_items['empty']
                        self.reminder_content_layout.remove_widget(item)
                        self.reminder_items.pop('empty')

                    self.display_reminder_title(title)



                elif mode == 'edit':
                    title, date, time, cycle = obj.save()
                    self.db_reminder.update(old_title, title, date, time, cycle)
                    self.reminder_data = self.db_reminder.retrieve()
                    if title in self.reminder_items:
                        item = self.reminder_items[title]
                        self.reminder_content_layout.remove_widget(item)
                        self.reminder_items.pop(title)
                    if 'empty' in self.reminder_items:
                        item = self.reminder_items['empty']
                        self.reminder_content_layout.remove_widget(item)
                        self.reminder_items.pop('empty')
                    if old_title in self.reminder_items:
                        item = self.reminder_items[old_title]
                        self.reminder_content_layout.remove_widget(item)
                        self.reminder_items.pop(old_title)

                    self.display_reminder_title(title)

                print(self.reminder_data)
                self.reminder_popup.dismiss()

            elif obj.save()==None:
                self.popup_err_msg_reminder()

            elif obj.save()=='valueerror':
                self.popup_err_msg_reminder('Invalid date or time!')


        def cancel(obj):
            self.reminder_popup.dismiss()

    def pop_management_list(self,*args):
        Snackbar(
            text="Loading...!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5,
            duration=1
        ).open()

        Clock.schedule_once(lambda x: self.pop_management_list_process(*args), .5)

    def pop_management_list_process(self, instance, title,amount='',date='',cycle='', mode='new'):

        Snackbar(
            text="Loading...!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5,
            duration=1
        ).open()

        if mode == 'new':
            obj = my_list_box()
        elif mode == 'edit':
            print(f"date in pop_management_list {date}")
            obj = my_list_box(title, amount,self.date_extractor(date),cycle, mode)
        self.management_list_popup = MDDialog(
            title=title,
            type='custom',
            content_cls=obj,
            buttons=[
                MDRaisedButton(text='Save', on_release=lambda x: save(obj, title)),
                MDRaisedButton(text='Cancel', on_release=lambda x: cancel(obj))
            ]
        )



        def open(instance):
            self.management_list_popup.open()

        Clock.schedule_once(open, 1)


        def save(obj, old_title):
            print(f"received {obj.save()}")
            if obj.save() not in [None, 'valueerror', 'inputerror']:

                if mode == 'new':
                    title, amount, cycle, date = obj.save()
                    self.db_management.insert(title, amount, cycle, date)
                    self.management_list_data = self.db_management.retrieve()
                    if title in self.management_list_items:
                        item = self.management_list_items[title]
                        self.management_list_content_layout.remove_widget(item)
                        self.management_list_items.pop(title)
                    if 'empty' in self.management_list_items:
                        item = self.management_list_items['empty']
                        self.management_list_content_layout.remove_widget(item)
                        self.management_list_items.pop('empty')
                    self.display_management_list_title(title)

                elif mode == 'edit':
                    title, amount, cycle, date = obj.save()
                    self.db_management.update(old_title, title, amount, cycle, date)
                    self.management_list_data = self.db_management.retrieve()

                    if title in self.management_list_items:
                        item = self.management_list_items[title]
                        self.management_list_content_layout.remove_widget(item)
                        self.management_list_items.pop(title)
                    if 'empty' in self.management_list_items:
                        item = self.management_list_items['empty']
                        self.management_list_content_layout.remove_widget(item)
                        self.management_list_items.pop('empty')
                    if old_title in self.management_list_items:
                        item = self.management_list_items[old_title]
                        self.management_list_content_layout.remove_widget(item)
                        self.management_list_items.pop(old_title)
                    self.display_management_list_title(title)

                self.update_total_income_expense()
                print(self.management_list_data)
                self.management_list_popup.dismiss()

            elif obj.save() == None:
                self.popup_err_msg_management_list()

            elif obj.save() == 'inputerror':
                self.popup_err_msg_management_list('Invalid amount or billing/purchase frequency cycle!')

            elif obj.save()=='valueerror':
                self.popup_err_msg_reminder('Invalid date or time!')

        def cancel(obj):
            self.management_list_popup.dismiss()

    def pop_income_list(self,*args):
        Snackbar(
            text="Loading...!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5,
            duration=1
        ).open()

        Clock.schedule_once(lambda x: self.pop_income_list_process(*args), .5)

    def pop_income_list_process(self, instance, title, amount='',date='',cycle='', mode='new'):

        Snackbar(
            text="Loading...!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5,
            duration=1
        ).open()

        if mode == 'new':
            obj = income_list_box()
        elif mode == 'edit':
            obj = income_list_box(title, amount,self.date_extractor(date),cycle, mode)
        self.income_list_popup = MDDialog(
            title=title,
            type='custom',
            content_cls=obj,
            buttons=[
                MDRaisedButton(text='Save', on_release=lambda x: save(obj, title)),
                MDRaisedButton(text='Cancel', on_release=lambda x: cancel(obj))
            ]
        )

        self.income_list_popup.open()
        def open(instance):
            self.income_list_popup.open()

        Clock.schedule_once(open, 1)


        def save(obj, old_title):
            print(f"received {obj.save()}")
            if obj.save() not in [None, 'valueerror', 'inputerror']:

                if mode == 'new':
                    title, amount, cycle, date = obj.save()
                    self.db_income.insert(title, amount, cycle, date)
                    self.income_list_data = self.db_income.retrieve()
                    if title in self.income_list_items:
                        item = self.income_list_items[title]
                        self.income_list_content_layout.remove_widget(item)
                        self.income_list_items.pop(title)
                    if 'empty' in self.income_list_items:
                        item = self.income_list_items['empty']
                        self.income_list_content_layout.remove_widget(item)
                        self.income_list_items.pop('empty')
                    self.display_income_list_title(title)
                elif mode == 'edit':
                    title, amount, cycle, date = obj.save()
                    self.db_income.update(old_title, title, amount, cycle, date)
                    self.income_list_data = self.db_income.retrieve()
                    if title in self.income_list_items:
                        item = self.income_list_items[title]
                        self.income_list_content_layout.remove_widget(item)
                        self.income_list_items.pop(title)
                    if 'empty' in self.income_list_items:
                        item = self.income_list_items['empty']
                        self.income_list_content_layout.remove_widget(item)
                        self.income_list_items.pop('empty')
                    if old_title in self.income_list_items:
                        item = self.income_list_items[old_title]
                        self.income_list_content_layout.remove_widget(item)
                        self.income_list_items.pop(old_title)
                    self.display_income_list_title(title)

                self.update_total_income_expense()
                print(self.income_list_data)
                self.income_list_popup.dismiss()

            elif obj.save() == None:
                self.popup_err_msg_income_list()

            elif obj.save() == 'inputerror':
                self.popup_err_msg_income_list('Invalid amount or income frequency cycle!')

            elif obj.save() == 'valueerror':
                self.popup_err_msg_reminder('Invalid date or time!')

        def cancel(obj):
            self.income_list_popup.dismiss()

    def pop_loan_list(self,*args):
        Snackbar(
            text="Loading...!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5,
            duration=1
        ).open()

        Clock.schedule_once(lambda x: self.pop_loan_list_process(*args), .5)

    def pop_loan_list_process(self, instance, title,amount='',date='',cycle='', mode='new'):

        Snackbar(
            text="Loading...!",
            snackbar_x="10dp",
            snackbar_y="10dp",
            size_hint_x=.5,
            duration=1
        ).open()

        print(f'data in pop_loan_list {date}')
        if mode == 'new':
            obj = loan_list_box()
        elif mode == 'edit':
            obj = loan_list_box(title, amount,self.date_extractor(date),cycle, mode)
        self.loan_list_popup = MDDialog(
            title=title,
            type='custom',
            content_cls=obj,
            buttons=[
                MDRaisedButton(text='Save', on_release=lambda x: save(obj, title)),
                MDRaisedButton(text='Cancel', on_release=lambda x: cancel(obj))
            ]
        )

        def open(instance):
            self.loan_list_popup.open()

        Clock.schedule_once(open, 1)

        def save(obj, old_title):
            print(f"received {obj.save()}")
            if obj.save() not in [None, 'valueerror', 'inputerror']:

                if mode == 'new':
                    title, amount, cycle, date = obj.save()
                    self.db_loan.insert(title, amount, cycle, date)
                    self.loan_list_data = self.db_loan.retrieve()
                    if title in self.loan_list_items:
                        item = self.loan_list_items[title]
                        self.loan_list_content_layout.remove_widget(item)
                        self.loan_list_items.pop(title)
                    if 'empty' in self.loan_list_items:
                        item = self.loan_list_items['empty']
                        self.loan_list_content_layout.remove_widget(item)
                        self.loan_list_items.pop('empty')
                    self.display_loan_list_title(title)

                elif mode == 'edit':
                    title, amount, cycle, date = obj.save()
                    self.db_loan.update(old_title, title, amount, cycle, date)
                    self.loan_list_data = self.db_loan.retrieve()
                    if title in self.loan_list_items:
                        item = self.loan_list_items[title]
                        self.loan_list_content_layout.remove_widget(item)
                        self.loan_list_items.pop(title)
                    if 'empty' in self.loan_list_items:
                        item = self.loan_list_items['empty']
                        self.loan_list_content_layout.remove_widget(item)
                        self.loan_list_items.pop('empty')
                    if old_title in self.loan_list_items:
                        item = self.loan_list_items[old_title]
                        self.loan_list_content_layout.remove_wdget(item)
                        self.loan_list_items.pop(old_title)
                    self.display_loan_list_title(title)

                self.update_total_income_expense()
                print(self.loan_list_data)
                self.loan_list_popup.dismiss()

            elif obj.save() == None:
                self.popup_err_msg_loan_list()


            elif obj.save() == 'inputerror':

                self.popup_err_msg_loan_list('Invalid amount or billing/purchase frequency cycle!')


            elif obj.save() == 'valueerror':

                self.popup_err_msg_reminder('Invalid date or time!')

        def cancel(obj):
            self.loan_list_popup.dismiss()

    def delete_notes_page(self,instance,name):
        print(f'deleting {name}')
        print(self.items)
        item = self.items[name]
        self.notes_content_layout.remove_widget(item)
        del self.items[name]
        self.db_notes.delete(name)
        self.notes_data=self.db_notes.retrieve()
        if len(self.items)==0:
            self.empty_notes=False
            self.empty_search()


    def delete_todo_page(self,instance,name):
        print(f'deleting {name}')
        item = self.todo_items[name]
        self.todo_content_layout.remove_widget(item)
        del self.todo_items[name]
        self.db_todo.delete(name)
        self.todo_data = self.db_todo.retrieve()
        if len(self.todo_items)==0:
            self.empty_todo=False
            self.empty_todo_search()

    def delete_reminder_page(self,instance,name):
        print(f'deleting {name}')
        item = self.reminder_items[name]
        self.reminder_content_layout.remove_widget(item)
        del self.reminder_items[name]
        self.db_reminder.delete(name)
        self.reminder_data = self.db_reminder.retrieve()
        if len(self.reminder_items)==0:
            self.empty_reminder=False
            self.empty_reminder_search()

    def delete_management_list_page(self,instance,name):
        print(f'deleting {name}')
        item = self.management_list_items[name]
        self.management_list_content_layout.remove_widget(item)
        del self.management_list_items[name]
        self.db_management.delete(name)
        self.management_list_data = self.db_management.retrieve()
        if len(self.management_list_items)==0:
            self.empty_management_list=False
            self.empty_management_list_search()

        self.update_total_income_expense()


    def delete_income_list_page(self,instance,name):
        print(f'deleting {name}')
        item = self.income_list_items[name]
        self.income_list_content_layout.remove_widget(item)
        del self.income_list_items[name]
        self.db_income.delete(name)
        self.income_list_data = self.db_income.retrieve()
        if len(self.income_list_items)==0:
            self.empty_income_list=False
            self.empty_income_list_search()

        self.update_total_income_expense()


    def delete_loan_list_page(self,instance,name):
        print(f'deleting {name}')
        item=self.loan_list_items[name]
        self.loan_list_content_layout.remove_widget(item)
        del self.loan_list_items[name]
        self.db_loan.delete(name)
        self.loan_list_data = self.db_loan.retrieve()
        print('deleted')
        if len(self.loan_list_items)==0:
            self.empty_loan_list=False
            self.empty_loan_list_search()

        self.update_total_income_expense()


    def show_notes_page(self,instance,name):
        self.view_note_bar.title=name
        self.note_read_title.text=name
        self.note_read_content.text=self.notes_data[name][0]
        self.view_note_layout.md_bg_color=self.notes_data[name][1]
        self.change_screen('View_note')

    def save_note(self,instance,title,detail,color_data):
        if title.strip() != '' and detail.strip() != '':
            print('no change' if not self.check_unsaved_notes() else 'changed')
            if self.check_unsaved_notes():
                if self.old_note_title!='':
                    if self.old_note_title in self.items:
                        self.delete_notes_page(None, self.old_note_title)
                    self.db_notes.update(self.old_note_title,title,detail,color=color_data)
                    self.old_note_title = ''

                self.db_notes.insert(title,detail, color=color_data)
                self.notes_data=self.db_notes.retrieve()
                self.color_data=[1,1,1,0]
                self.color_saved=False
                self.clear_note_cache()
                self.change_screen('Notes')
                if 'empty' in self.items:
                    item = self.items['empty']
                    self.notes_content_layout.remove_widget(item)
                    self.items.pop('empty')
                if title in self.items:
                    item = self.items[title]
                    self.notes_content_layout.remove_widget(item)
                self.display_notes_title(title)


            else:
                self.change_screen('Notes')
        else:
            self.save_notes_popup_box = MDDialog(
                title='Alert!',
                text='One of the fields are empty please fill that and save!',
                type='alert',
                buttons=[
                    MDRaisedButton(text='Ok', on_release=self.ok_notes_popup),
                ]
            )
            self.save_notes_popup_box.open()

    def popup_err_msg_todo(self,err=''):
        if err=='':
            err='One of the fields are empty please fill that and save!'

        self.save_todo_popup_box = MDDialog(
            title='Alert!',
            text=err,
            type='alert',
            buttons=[
                MDRaisedButton(text='Ok', on_release=self.ok_todo_popup),
            ]
        )
        self.save_todo_popup_box.open()

    def popup_err_msg_reminder(self,err=''):
        if err=='':
            err='One of the fields are empty please fill that and save!'

        self.save_reminder_popup_box = MDDialog(
            title='Alert!',
            text=err,
            type='alert',
            buttons=[
                MDRaisedButton(text='Ok', on_release=self.ok_reminder_popup),
            ]
        )
        self.save_reminder_popup_box.open()

    def popup_err_msg_management_list(self, err=''):
        if err == '':
            err = 'One of the fields are empty please fill that and save!'

        self.save_management_list_popup_box = MDDialog(
            title='Alert!',
            text=err,
            type='alert',
            buttons=[
                MDRaisedButton(text='Ok', on_release=self.ok_management_list_popup),
            ]
        )
        self.save_management_list_popup_box.open()

    def popup_err_msg_income_list(self, err=''):
        if err == '':
            err = 'One of the fields are empty please fill that and save!'

        self.save_income_list_popup_box = MDDialog(
            title='Alert!',
            text=err,
            type='alert',
            buttons=[
                MDRaisedButton(text='Ok', on_release=self.ok_income_list_popup),
            ]
        )
        self.save_income_list_popup_box.open()

    def popup_err_msg_loan_list(self, err=''):
        if err == '':
            err = 'One of the fields are empty please fill that and save!'

        self.save_loan_list_popup_box = MDDialog(
            title='Alert!',
            text=err,
            type='alert',
            buttons=[
                MDRaisedButton(text='Ok', on_release=self.ok_loan_list_popup),
            ]
        )
        self.save_loan_list_popup_box.open()


    def discard_note(self,instance,title,detail):
        if title.strip()!='' and detail.strip()!='':
            if self.check_unsaved_notes():
                self.notes_popup_box=MDDialog(
                    title='Alert!',
                    text='Do you wanna save changes?',
                    type='alert',
                    buttons=[
                        MDRaisedButton(text='Yes',on_release=self.yes_notes_popup),
                        MDRaisedButton(text='No',on_release=self.no_notes_popup),
                        MDRaisedButton(text='Cancel',on_release=self.cancel_notes_popup),
                    ]
                )
                self.notes_popup_box.open()
                print('popped')

            else:
                self.change_screen('Notes')
        else:
            self.change_screen('Notes')

    def ok_notes_popup(self,instance):
        self.save_notes_popup_box.dismiss()

    def yes_notes_popup(self,instance):
        self.notes_popup_box.dismiss()
        self.save_note(None,self.note_title.text,self.note_content.text,self.color_data)
        self.change_screen('Notes')

    def no_notes_popup(self,instance):
        self.notes_popup_box.dismiss()
        self.color_data = [1,1,1,0]
        self.clear_note_cache()
        self.change_screen('Notes')

    def cancel_notes_popup(self,instance):
        self.notes_popup_box.dismiss()

    def ok_todo_popup(self,instance):
        self.save_todo_popup_box.dismiss()

    def ok_reminder_popup(self, instance):
        self.save_reminder_popup_box.dismiss()

    def ok_management_list_popup(self, instance):
        self.save_management_list_popup_box.dismiss()

    def ok_income_list_popup(self, instance):
        self.save_income_list_popup_box.dismiss()

    def ok_loan_list_popup(self, instance):
        self.save_loan_list_popup_box.dismiss()

    def menu(self,instance):
        print('menu is called')

    def hide_search_bar(self):
        self.search_bar.text = ''
        self.search_bar.opacity = 0
        if self.refresh_note_touch:
            self.refresh_note.opacity = 0
            self.refresh_note_touch = False
        self.search = False

    def hide_todo_search_bar(self):
        self.todo_search_bar.text = ''
        self.todo_search_bar.opacity = 0
        if self.refresh_todo_touch:
            self.refresh_todo.opacity = 0
            self.refresh_todo_touch = False
        self.todo_search = False

    def hide_reminder_search_bar(self):
        self.reminder_search_bar.text = ''
        self.reminder_search_bar.opacity = 0
        if self.refresh_reminder_touch:
            self.refresh_reminder.opacity = 0
            self.refresh_reminder_touch = False
        self.reminder_search = False

    def hide_management_list_search_bar(self):
        self.management_list_search_bar.text = ''
        self.management_list_search_bar.opacity = 0
        if self.refresh_management_list_touch:
            self.refresh_management_list.opacity = 0
            self.refresh_management_list_touch = False
        self.management_list_search = False

    def hide_income_list_search_bar(self):
        self.income_list_search_bar.text = ''
        self.income_list_search_bar.opacity = 0
        if self.refresh_income_list_touch:
            self.refresh_income_list.opacity = 0
            self.refresh_income_list_touch = False
        self.income_list_search = False

    def hide_loan_list_search_bar(self):
        self.loan_list_search_bar.text = ''
        self.loan_list_search_bar.opacity = 0
        if self.refresh_loan_list_touch:
            self.refresh_loan_list.opacity = 0
            self.refresh_loan_list_touch = False
        self.loan_list_search = False

    def close_note_search_and_refresh(self,instance):
        print('refresh touched',self.refresh_note_touch)
        if self.refresh_note_touch:
            self.refresh_note_touch=False
        else:
            self.refresh_note_touch=True
        self.hide_search_bar()
        self.show_notes_title()

    def close_todo_search_and_refresh(self,instance):
        print('refresh touched',self.refresh_todo_touch)
        if self.refresh_todo_touch:
            self.refresh_todo_touch=False
        else:
            self.refresh_todo_touch=True
        self.hide_todo_search_bar()
        self.show_todo_title()

    def close_reminder_search_and_refresh(self,instance):
        print('refresh touched',self.refresh_reminder_touch)
        if self.refresh_reminder_touch:
            self.refresh_reminder_touch=False
        else:
            self.refresh_reminder_touch=True
        self.hide_reminder_search_bar()
        self.show_reminder_title()

    def close_management_list_search_and_refresh(self,instance):
        print('refresh touched',self.refresh_management_list_touch)
        if self.refresh_management_list_touch:
            self.refresh_management_list_touch=False
        else:
            self.refresh_management_list_touch=True
        self.hide_management_list_search_bar()
        self.show_management_list_title(custom=self.management_custom,data=self.custom_data)

    def close_income_list_search_and_refresh(self,instance):
        print('refresh touched',self.refresh_income_list_touch)
        if self.refresh_income_list_touch:
            self.refresh_income_list_touch=False
        else:
            self.refresh_income_list_touch=True
        self.hide_income_list_search_bar()
        self.show_income_list_title()

    def close_loan_list_search_and_refresh(self,instance):
        print('refresh touched', self.refresh_loan_list_touch)
        if self.refresh_loan_list_touch:
            self.refresh_loan_list_touch = False
        else:
            self.refresh_loan_list_touch = True
        self.hide_loan_list_search_bar()
        self.show_loan_list_title(custom=self.loan_custom, data=self.loan_custom_data)

    def search_icon(self,instance):
        if self.search:
            if self.search_bar.text!='':
                self.search_notes(self.search_bar.text)
                self.search_bar.text = ''
            else:
                self.hide_search_bar()
        else:
            self.search=True
            self.search_bar.opacity=1
            if self.refresh_note_touch:
                self.refresh_note.opacity=1
                self.refresh_note_touch=False

    def todo_search_icon(self,instance):
        print('todo search is called')
        if self.todo_search:
            if self.todo_search_bar.text!='':
                self.search_todo(self.todo_search_bar.text)
                self.todo_search_bar.text = ''
            else:
                self.hide_todo_search_bar()
        else:
            self.todo_search=True
            self.todo_search_bar.opacity=1
            if self.refresh_todo_touch:
                self.refresh_todo.opacity=1
                self.refresh_todo_touch=False

    def reminder_search_icon(self,instance):
        print('reminder search is called')
        if self.reminder_search:
            if self.reminder_search_bar.text!='':
                self.search_reminder(self.reminder_search_bar.text)
                self.reminder_search_bar.text = ''
            else:
                self.hide_reminder_search_bar()
        else:
            self.reminder_search=True
            self.reminder_search_bar.opacity=1
            if self.refresh_reminder_touch:
                self.refresh_reminder.opacity=1
                self.refresh_reminder_touch=False

    def management_list_search_icon(self,instance,custom=False,data=''):
        print('management search is called')
        if self.management_list_search:
            if self.management_list_search_bar.text!='':
                self.search_management_list(self.management_list_search_bar.text,custom,data)
                self.management_list_search_bar.text = ''
            else:
                self.hide_management_list_search_bar()
        else:
            self.management_list_search=True
            self.management_list_search_bar.opacity=1
            if self.refresh_management_list_touch:
                self.refresh_management_list.opacity=1
                self.refresh_management_list_touch=False

    def income_list_search_icon(self,instance):
        print('management search is called')
        if self.income_list_search:
            if self.income_list_search_bar.text!='':
                self.search_income_list(self.income_list_search_bar.text)
                self.income_list_search_bar.text = ''
            else:
                self.hide_income_list_search_bar()
        else:
            self.income_list_search=True
            self.income_list_search_bar.opacity=1
            if self.refresh_income_list_touch:
                self.refresh_income_list.opacity=1
                self.refresh_income_list_touch=False

    def loan_list_search_icon(self,instance,custom=False,data=''):
        print('loan search is called')
        if self.loan_list_search:
            if self.loan_list_search_bar.text!='':
                self.search_loan_list(self.loan_list_search_bar.text,custom,data)
                self.loan_list_search_bar.text = ''
            else:
                self.hide_loan_list_search_bar()
        else:
            self.loan_list_search=True
            self.loan_list_search_bar.opacity=1
            if self.refresh_loan_list_touch:
                self.refresh_loan_list.opacity=1
                self.refresh_loan_list_touch=False

    def empty_search(self):
        if self.empty_notes==False:
            self.empty_label = MDLabel(text='No items', halign='center')
            self.notes_content_layout.add_widget(self.empty_label)
            self.items['empty'] = self.empty_label
            self.empty_notes=True
            print('no items is ON')

    def empty_todo_search(self):
        if self.empty_todo==False:
            self.empty_todo_label = MDLabel(text='No items', halign='center')
            self.todo_content_layout.add_widget(self.empty_todo_label)
            self.todo_items['empty'] = self.empty_todo_label
            self.empty_todo = False

    def empty_reminder_search(self):
        print('empty reminder called')
        if self.empty_reminder==False:
            self.empty_reminder_label = MDLabel(text='No items', halign='center')
            self.reminder_content_layout.add_widget(self.empty_reminder_label)
            self.reminder_items['empty'] = self.empty_reminder_label
            self.empty_reminder = False

    def empty_management_list_search(self):
        print('empty management_list called')
        if self.empty_management_list==False:
            self.empty_management_list_label = MDLabel(text='No items', halign='center')
            self.management_list_content_layout.add_widget(self.empty_management_list_label)
            self.management_list_items['empty'] = self.empty_management_list_label
            self.empty_management_list = False

    def empty_income_list_search(self):
        print('empty income_list called')
        if self.empty_income_list==False:
            self.empty_income_list_label = MDLabel(text='No items', halign='center')
            self.income_list_content_layout.add_widget(self.empty_income_list_label)
            self.income_list_items['empty'] = self.empty_income_list_label
            self.empty_income_list = False

    def empty_loan_list_search(self):
        print('empty loan_list called')
        if self.empty_loan_list==False:
            self.empty_loan_list_label = MDLabel(text='No items', halign='center')
            self.loan_list_content_layout.add_widget(self.empty_loan_list_label)
            self.loan_list_items['empty'] = self.empty_loan_list_label
            self.empty_loan_list = False

    def search_notes(self,data):

        for deletable in self.items:
            self.notes_content_layout.remove_widget(self.items[deletable])

        correct=0
        self.refresh_note.opacity = 1
        for item in self.notes_data:
            print(item)
            if data.lower() in item.lower():
                correct += 1
                print(item)
                self.display_notes_title(item)
        if correct==0:
            print('Empty notes will print \'no items\' if False and we\'re having',self.empty_notes)
            self.empty_notes = False
            self.empty_search()


        if correct!=0:
            try:
                self.notes_content_layout.remove_widget(self.empty_label)
            except AttributeError:
                pass
            self.empty_notes=False
            print('no items is OFF')

    def search_todo(self,data):
        for deletable in self.todo_items:
            self.todo_content_layout.remove_widget(self.todo_items[deletable])
        correct=0
        self.refresh_todo.opacity = 1
        for item in self.todo_data:
            print(item)
            if data.lower() in item.lower():
                correct += 1
                print(item)
                self.display_todo_title(item)
        if correct==0:
            print(f'todo is now empty {self.empty_todo}')
            self.empty_todo = False
            self.empty_todo_search()

        if correct!=0:
            try:
                self.todo_content_layout.remove_widget(self.empty_todo_label)
            except AttributeError:
                pass
            self.empty_todo=False

    def search_reminder(self,data):
        for deletable in self.reminder_items:
            self.reminder_content_layout.remove_widget(self.reminder_items[deletable])
        correct=0
        self.refresh_reminder.opacity = 1
        for item in self.reminder_data:
            print(item)
            if data.lower() in item.lower():
                correct += 1
                print(item)
                self.display_reminder_title(item)

        if correct==0:
            self.empty_reminder = False
            print('empty reminder search')
            self.empty_reminder_search()

        if correct!=0:
            try:
                self.reminder_content_layout.remove_widget(self.empty_reminder_label)
            except AttributeError:
                pass
            self.empty_reminder=False

    def search_management_list(self,data,custom=False,items=''):

        for deletable in self.management_list_items:
            self.management_list_content_layout.remove_widget(self.management_list_items[deletable])
        correct = 0
        self.refresh_management_list.opacity = 1
        print(f"custom in search_management_list : {custom}")
        if custom:

            for item in items:
                print(item)
                if data.lower() in item.lower():
                    correct += 1
                    print(item)
                    self.display_management_list_title(item)

        else:
            for item in self.management_list_data:
                print(item)
                if data.lower() in item.lower():
                    correct += 1
                    print(item)
                    self.display_management_list_title(item)

        if correct==0:
            self.empty_management_list = False
            print('empty management_list search')
            self.empty_management_list_search()

        if correct!=0:
            try:
                self.management_list_content_layout.remove_widget(self.empty_management_list_label)
            except AttributeError:
                pass
            self.empty_management_list=False

    def search_income_list(self,data):
        for deletable in self.income_list_items:
            self.income_list_content_layout.remove_widget(self.income_list_items[deletable])
        correct=0
        self.refresh_income_list.opacity = 1
        for item in self.income_list_data:
            print(item)
            if data.lower() in item.lower():
                correct += 1
                print(item)
                self.display_income_list_title(item)

        if correct==0:
            self.empty_income_list = False
            print('empty income_list search')
            self.empty_income_list_search()

        if correct!=0:
            try:
                self.income_list_content_layout.remove_widget(self.empty_income_list_label)
            except AttributeError:
                pass
            self.empty_management_list=False

    def search_loan_list(self,data,custom=False,items=''):
        for deletable in self.loan_list_items:
            self.loan_list_content_layout.remove_widget(self.loan_list_items[deletable])
        correct=0
        self.refresh_loan_list.opacity = 1
        if custom:
            for item in items:
                print(item)
                if data.lower() in item.lower():
                    correct += 1
                    print(item)
                    self.display_loan_list_title(item)

        else:
            for item in self.loan_list_data:
                print(item)
                if data.lower() in item.lower():
                    correct += 1
                    print(item)
                    self.display_loan_list_title(item)

        if correct==0:
            self.empty_loan_list = False
            print('empty loan_list search')
            self.empty_loan_list_search()

        if correct!=0:
            try:
                self.loan_list_content_layout.remove_widget(self.empty_loan_list_label)
            except AttributeError:
                pass
            self.empty_loan_list=False

    def show_notes_title(self):
        try:
            self.notes_content_layout.remove_widget(self.empty_label)
        except AttributeError:
            pass
        for deletable in self.items:
            self.notes_content_layout.remove_widget(self.items[deletable])
        self.notes_dict_to_item(self.notes_data)

    def show_todo_title(self):
        try:
            self.todo_content_layout.remove_widget(self.empty_todo_label)
        except AttributeError:
            pass
        for deletable in self.todo_items:
            self.todo_content_layout.remove_widget(self.todo_items[deletable])
        self.todo_dict_to_item(self.todo_data)

    def show_reminder_title(self):
        try:
            self.reminder_content_layout.remove_widget(self.empty_reminder_label)
        except AttributeError:
            pass
        for deletable in self.reminder_items:
            self.reminder_content_layout.remove_widget(self.reminder_items[deletable])
        self.reminder_dict_to_item(self.reminder_data)

    def show_management_list_title(self,custom=False,data=''):

        try:
            self.management_list_content_layout.remove_widget(self.empty_management_list_label)
        except AttributeError:
            pass
        for deletable in self.management_list_items:
            self.management_list_content_layout.remove_widget(self.management_list_items[deletable])

        if custom:
            self.management_list_dict_to_item(data)
        else:
            self.management_list_dict_to_item(self.management_list_data)

    def show_income_list_title(self):
        try:
            self.income_list_content_layout.remove_widget(self.empty_income_list_label)
        except AttributeError:
            pass
        for deletable in self.income_list_items:
            self.income_list_content_layout.remove_widget(self.income_list_items[deletable])
        self.income_list_dict_to_item(self.income_list_data)

    def show_loan_list_title(self, custom=False, data=''):
        try:
            self.loan_list_content_layout.remove_widget(self.empty_loan_list_label)
        except AttributeError:
            pass
        for deletable in self.loan_list_items:
            self.loan_list_content_layout.remove_widget(self.loan_list_items[deletable])

        if custom:
            self.loan_list_dict_to_item(data)
        else:
            self.loan_list_dict_to_item(self.loan_list_data)

    def notes_dict_to_item(self,dict_data):
        if len(dict_data)==0:
            print('note is empty')
            self.empty_notes = False
            print('no items is OFF')
            self.empty_search()

        elif len(dict_data)>0:
            self.empty_notes = False
            for item in dict_data:
                self.display_notes_title(item)

    def todo_dict_to_item(self,todo_data):
        if len(todo_data)==0:
            print('todo is empty')
            self.empty_todo = False
            self.empty_todo_search()

        elif len(todo_data)>0:
            self.empty_todo = False
            for item in todo_data:
                self.display_todo_title(item)

    def reminder_dict_to_item(self,reminder_data):
        if len(reminder_data)==0:
            print('reminder is empty')
            self.empty_reminder = False
            self.empty_reminder_search()
            self.empty_reminder = True

        elif len(reminder_data) > 0:
            self.empty_reminder = False
            for item in reminder_data:
                self.display_reminder_title(item)

    def management_list_dict_to_item(self,management_list_data):
        if len(management_list_data)==0:
            print('management_list is empty')
            self.empty_management_list = False
            self.empty_management_list_search()
            self.empty_management_list = True

        elif len(management_list_data) > 0:
            self.empty_management_list = False
            for item in management_list_data:
                self.display_management_list_title(item)

    def income_list_dict_to_item(self,income_list_data):
        if len(income_list_data)==0:
            print('income_list is empty')
            self.empty_income_list = False
            self.empty_income_list_search()
            self.empty_income_list = True

        elif len(income_list_data) > 0:
            self.empty_income_list = False
            for item in income_list_data:
                self.display_income_list_title(item)

    def loan_list_dict_to_item(self,loan_list_data):
        if len(loan_list_data)==0:
            print('loan_list is empty')
            self.empty_loan_list = False
            self.empty_loan_list_search()
            self.empty_loan_list = True

        elif len(loan_list_data) > 0:
            self.empty_loan_list = False
            for item in loan_list_data:
                self.display_loan_list_title(item)

    def display_notes_title(self,data):
        print(data)
        item = MDExpansionPanel(
            content=self.notes_view_del(data),
            panel_cls=MDExpansionPanelOneLine(
                height=dp(20),
                radius=(dp(5), dp(5), dp(0), dp(0)),
                divider=None,
                md_bg_color=self.menu_parent_color,
                on_release=lambda x:x,
                text="  "+data,
            )
        )
        self.items.update({data:item})
        self.notes_content_layout.add_widget(item)

    def display_todo_title(self,data):
        print(data)
        datetime_status=self.valid_datetime(self.todo_data[data][0],self.todo_data[data][1])
        item = MDExpansionPanel(
            icon='' if datetime_status else 'alert-circle',
            content=self.todo_edit_del(data),
            panel_cls=MDExpansionPanelTwoLine(
                height=dp(20),
                radius=(dp(5), dp(5), dp(0), dp(0)),
                divider=None,
                md_bg_color=self.menu_parent_color if datetime_status else (238 / 255, 11 / 255, 11 / 255, 0.8),
                on_release=lambda x:x,
                text="  "+data,
                secondary_text='  ' if datetime_status else '  OVERDUE'
            )
        )
        self.todo_items.update({data:item})
        self.todo_content_layout.add_widget(item)

    def display_reminder_title(self,data):
        print(data)
        item = MDExpansionPanel(
            content=self.reminder_edit_del(data),
            panel_cls=MDExpansionPanelOneLine(
                height=dp(20),
                radius=(dp(5), dp(5), dp(0), dp(0)),
                divider=None,
                md_bg_color=self.menu_parent_color,
                on_release=lambda x:x,
                text="  "+data,
            )
        )
        self.reminder_items.update({data:item})
        self.reminder_content_layout.add_widget(item)

    def display_management_list_title(self,data):
        print(data)
        print(f"data is {self.management_list_data[data][2]}")
        datetime_status = self.valid_datetime(self.management_list_data[data][2], time=False)
        item = MDExpansionPanel(
            icon='' if datetime_status else 'alert-circle',
            content=self.management_list_edit_del(data),
            panel_cls=MDExpansionPanelTwoLine(
                height=dp(20),
                radius=(dp(5), dp(5), dp(0), dp(0)),
                divider=None,
                md_bg_color=self.menu_parent_color if datetime_status else (238 / 255, 11 / 255, 11 / 255, 0.8),
                on_release=lambda x:x,
                text="  "+data,
                secondary_text='  Amount - '+self.management_list_data[data][0]
            )
        )
        self.management_list_items.update({data:item})
        self.management_list_content_layout.add_widget(item)

    def display_income_list_title(self,data):
        print(data)
        item = MDExpansionPanel(
            content=self.income_list_edit_del(data),
            panel_cls=MDExpansionPanelTwoLine(
                height=dp(20),
                radius=(dp(5), dp(5), dp(0), dp(0)),
                divider=None,
                md_bg_color=self.menu_parent_color,
                on_release=lambda x:x,
                text="  "+data,
                secondary_text='  Amount - '+self.income_list_data[data][0]
            )
        )
        self.income_list_items.update({data:item})
        self.income_list_content_layout.add_widget(item)

    def display_loan_list_title(self,data):
        datetime_status = self.valid_datetime(self.loan_list_data[data][2], time=False)
        if datetime_status:

            print('date status is good',self.loan_list_data[data][2])
            color=self.menu_parent_color
        else:

            print('date status is overdue',self.loan_list_data[data][2])
            color=(238 / 255, 11 / 255, 11 / 255, 0.8)
        item = MDExpansionPanel(
            content=self.loan_list_edit_del(data),
            icon='' if datetime_status else 'alert-circle',
            panel_cls=MDExpansionPanelTwoLine(
                height=dp(20),
                radius=(dp(5), dp(5), dp(0), dp(0)),
                divider=None,
                md_bg_color=color,
                on_release=lambda x:x,
                text="  "+data,
                secondary_text='  Amount - '+self.loan_list_data[data][0]
            )
        )
        self.loan_list_items.update({data:item})
        self.loan_list_content_layout.add_widget(item)

    def valid_datetime(self,date,time=True):
        date = self.date_extractor(date)
        if time:
            print(time)
            time = self.time_extractor(time)

            hour, minute, second = tuple(map(lambda x: int(x), time.split(':')))
            present_hour, present_minute, present_second = datetime.now().hour, datetime.now().minute, datetime.now().second

        day,month,year=tuple(map(lambda x: int(x),date.split('-')))
        present_day, present_month, present_year = datetime.now().day, datetime.now().month, datetime.now().year

        if year >= present_year:
            if year==present_year:
                if month >= present_month:
                    if month==present_month:
                        if day>=present_day:
                            if day==present_day:
                                if time == False:
                                    return True
                                if hour >= present_hour:
                                    if hour == present_hour:
                                        if minute >= present_minute:
                                            if minute == present_minute:
                                                if second > present_second:
                                                    return True
                                                return False
                                            return True
                                        return False
                                    return True
                                return False
                            return True
                        return False
                    return True
                return False
            return True
        return False



    def create_note(self,instance,name):
        self.new_note_bar.title = 'New note'
        self.note_new_title.text = 'New note'
        self.new_note_layout.md_bg_color=[1,1,1,0]
        self.change_screen(name)
        self.hide_search_bar()

    def empty(self,instance):
        pass

    def switch_tab(self):
        print("Switch tab is called!")

    def all_notes(self):
        pass

if __name__ == '__main__':
    Noteable().run()