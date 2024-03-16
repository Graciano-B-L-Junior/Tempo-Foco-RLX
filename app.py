import flet as ft
import datetime
import asyncio
from enum import Enum
import copy
from pathlib import Path
import pygame

all_data={
    "tempo_hrs":0,
    "tempo_min":0,
    "tempo_seg":0,
    "foco_min":0,
    "rlx_min":0,
}



def play_sound(sound_path=""):
    sound = sound_path
    pygame.init()
    pygame.mixer.music.load(sound_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.quit()


tempo_hrs_ref = ft.Ref[ft.Dropdown]()
tempo_min_ref = ft.Ref[ft.Dropdown]()
tempo_seg_ref = ft.Ref[ft.Dropdown]()

foco_min_ref = ft.Ref[ft.Dropdown]()

rlx_min_ref = ft.Ref[ft.Dropdown]()


async def main(page: ft.Page):
    page.title="Tempo-Focus-RLX"
    page.window_max_width = 1000
    page.window_max_height = 700

    # page.theme = ft.theme.Theme(color_scheme_seed='white')
    page.padding=0
    await page.update_async()

    # await action_page(page)
    await home_page(page)

async def home_page(page:ft.Page):
    top = ft.Row([
        ft.Text("What are you gonna do?",size=20)
    ],alignment=ft.MainAxisAlignment.CENTER)
    
    await page.add_async()

    middle=ft.Row([
        ft.Container(
            ft.Column([
                ft.Text("Tempo",size=20),
                ft.Icon(name=ft.icons.SCHEDULE,size=70),
                ft.Row([
                    ft.Dropdown(
                        ref=tempo_hrs_ref,
                        options=generate_options(99),
                        width=100,
                        label="Hrs",
                        on_change=change_all_data_value,                    
                    ),
                    ft.Dropdown(
                        ref=tempo_min_ref,
                        options=generate_options(59),
                        width=100,
                        label="Min",
                        on_change=change_all_data_value
                    ),
                    # ft.Dropdown(
                    #     ref=tempo_seg_ref,
                    #     options=generate_options(59),
                    #     width=100,
                    #     label="Sec",
                    #     on_change=change_all_data_value
                    # )
                ])
            ],alignment=ft.MainAxisAlignment.CENTER
            ,horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.colors.BLUE_GREY_50,
            border_radius=10,
            padding=20,
        ),
        ft.Container(
            ft.Column([
                ft.Text("Foco",size=20),
                ft.Icon(name=ft.icons.TIMER_SHARP,size=70),
                ft.Dropdown(
                    ref=foco_min_ref,
                    options=generate_options(59),
                    width=100,
                    label="Min",
                    on_change=change_all_data_value
                )
            ],alignment=ft.MainAxisAlignment.CENTER
            ,horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.colors.BLUE_GREY_50,
            border_radius=10,
            padding=20,
        ),
        ft.Container(
            ft.Column([
                ft.Text("RLX",size=20),
                ft.Icon(name=ft.icons.NATURE_PEOPLE_OUTLINED,size=70),
                ft.Dropdown(
                    ref=rlx_min_ref,
                    options=generate_options(59),
                    width=100,
                    label="Min",
                    on_change=change_all_data_value
                )
            ],alignment=ft.MainAxisAlignment.CENTER
            ,horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.colors.BLUE_GREY_50,
            border_radius=10,
            padding=20,
            
            
        )
    ],alignment=ft.MainAxisAlignment.CENTER
     ,spacing=100)
    
    button=ButtonStartHomePage(page)

    bottom=ft.Row([
        button
    ],alignment=ft.MainAxisAlignment.CENTER)
    
    column=ft.Column([
        top,ft.Divider(),
        middle,
        ft.Divider(),
        bottom
    ])
    container = ft.Container(width=1000,height=700,content=column,bgcolor=ft.colors.BLUE_GREY_200,padding=10)

    await page.add_async(container)
    tempo_hrs_ref.current.value=1
    tempo_min_ref.current.value=30
    # tempo_seg_ref.current.value=0

    foco_min_ref.current.value=20

    rlx_min_ref.current.value=5

    await page.update_async()

async def action_page(page: ft.Page):
    aux=datetime.datetime.now()
    aux_tempo=datetime.datetime.combine(aux.date(),datetime.time(hour=all_data["tempo_hrs"],
                                                                 minute=all_data["tempo_min"],
                                                                 second=all_data["tempo_seg"]))
    aux_focus=datetime.datetime.combine(aux.date(),datetime.time(hour=0,
                                                            minute=all_data["foco_min"],
                                                            second=0))
    aux_rlx=datetime.datetime.combine(aux.date(),datetime.time(hour=0,
                                                            minute=all_data["rlx_min"],
                                                            second=0))

    handler=CountDownHandler()

    count_down_tempo = Countdown_timer(aux_tempo,handler)
    count_down_focus = Countdown_timer(aux_focus,handler)
    count_down_rlx = Countdown_timer(aux_rlx,handler)

    handler.set_countdown_timers(count_down_tempo,
                                 count_down_focus,
                                 count_down_rlx)
    
    handler.init_countdown_timer_tempo_focus_and_rlx()

    button_stop_all = ButtonStopCountdown(countdown_handler=handler)

    top=ft.Column([
        ft.Row([
            ReturnHomePageButton(page),
            ft.Text("Back",size=20),
        ]),
        ft.Divider()
    ],horizontal_alignment=ft.CrossAxisAlignment.CENTER,)
    middle=ft.Row([
        ft.Column([
            ft.Text("Tempo",size=30),
            ft.Icon(name=ft.icons.SCHEDULE,size=70),
            count_down_tempo
        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ,spacing=15,width=150),
        ft.Column([
            ft.Text("Foco",size=30),
            ft.Icon(name=ft.icons.TIMER_SHARP,size=70),
            count_down_focus
        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ,spacing=15,width=150),
        ft.Column([
            ft.Text("RLX",size=30),
            ft.Icon(name=ft.icons.NATURE_PEOPLE_OUTLINED,size=70),
            count_down_rlx
        ],horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ,spacing=15,width=150)
    ],alignment=ft.MainAxisAlignment.CENTER
    ,spacing=100)

    button_middle = ft.Row([
        button_stop_all
    ],alignment=ft.MainAxisAlignment.CENTER,)
    await page.add_async(top,ft.Container(padding=35),middle,ft.Container(padding=20),button_middle)

def change_all_data_value(e):
    all_data["tempo_hrs"]=tempo_hrs_ref.current.value
    all_data["tempo_min"]=tempo_min_ref.current.value
    # all_data["tempo_seg"]=tempo_seg_ref.current.value

    all_data["foco_min"]=foco_min_ref.current.value

    all_data["rlx_min"]=rlx_min_ref.current.value

def generate_options(qtd:int) -> list:
    options=[]
    for index in range(1,qtd+1):
        options.append(
            ft.dropdown.Option(f"{index}")
        )
    return options


class Countdown_timer(ft.UserControl):

    def __init__(self,time:datetime.datetime,handler=None,tag=""):
        super().__init__()
        self.time = time
        self.task:asyncio.Task = None
        self.handler=handler
        self.tag=tag
        self.over=False
        self.running=False
        self.start_time=copy.copy(time)

    def build(self):
        self.countdown = ft.Text(size=30)
        return self.countdown
    
    async def did_mount_async(self):
        # self.running = False
        # asyncio.create_task(self.count_down_time())
        self.run_countdown()

    async def will_unmount_async(self):
        self.running = False

    def restart_timer(self):
        self.time=copy.copy(self.start_time)

    async def count_down_time(self):
        end_time = datetime.datetime.now()
        end_time=datetime.datetime.combine(end_time.date(),datetime.time(hour=0,minute=0,second=0))
        self.countdown.value=self.time.strftime("%H:%M:%S")
        await self.update_async()
        while self.time > end_time and self.running:
            self.countdown.value=self.time.strftime("%H:%M:%S")
            await self.update_async()
            await asyncio.sleep(1)
            self.time -= datetime.timedelta(seconds=1)
        if self.time <= end_time:
            self.countdown.value=self.time.strftime("%H:%M:%S")
            await self.update_async()
            self.over=True
            self.handler.receiving_alert_timer_is_over()
            self.running=False
            self.restart_timer()

    def run_countdown(self):
        self.task=asyncio.create_task(self.count_down_time())
        


    def change_state(self,stop_countdown:bool):
        if stop_countdown:
            self.running=False
            self.task.cancel()
        else:
            self.running=True
            self.run_countdown()
        
class ButtonStopCountdown(ft.UserControl):
    def __init__(self,countdown_handler):
        super().__init__()
        self.paused=False
        self.text_content = ft.Text("Pause",size=30)
        self.countdown_handler=countdown_handler

    def build(self):
        self.button_stop_countdown = ft.ElevatedButton(content=self.text_content,on_click=self.stop)
        return self.button_stop_countdown

    async def stop(self,e):
        self.paused = not self.paused
        self.text_content.value="Play" if self.paused else "Pause"
        self.countdown_handler.play_or_pause_countdown_timer(self.paused)
        await self.update_async()
    
class CountDownHandler:
    
    def __init__(self,countdown_timer_tempo:Countdown_timer=None,
                 countdown_timer_focus:Countdown_timer=None,
                 countdown_timer_rlx:Countdown_timer=None) -> None:
        self.countdown_timer_tempo=countdown_timer_tempo
        self.countdown_timer_focus=countdown_timer_focus
        self.countdown_timer_rlx=countdown_timer_rlx
        self.states=Enum('STATES',['FOCUS_TIME','RLX_TIME'])
        self.current_state=self.states.FOCUS_TIME
    
    def stop_focus_start_rlx(self):
        self.countdown_timer_focus.change_state(True)
        self.countdown_timer_rlx.change_state(False)
        self.current_state=self.states.RLX_TIME

    def stop_all_if_tempo_is_over(self):
        self.countdown_timer_tempo.change_state(True)
        self.countdown_timer_rlx.change_state(True)
        self.countdown_timer_focus.change_state(True)
        self.current_state=self.states.FOCUS_TIME
        

    def stop_rlx_start_focus(self):
        self.countdown_timer_focus.change_state(False)
        self.countdown_timer_rlx.change_state(True)
        self.current_state=self.states.FOCUS_TIME

    def set_countdown_timers(self,countdown_timer_tempo:Countdown_timer,
                 countdown_timer_focus:Countdown_timer,
                 countdown_timer_rlx:Countdown_timer):
        self.countdown_timer_tempo=countdown_timer_tempo
        self.countdown_timer_focus=countdown_timer_focus
        self.countdown_timer_rlx=countdown_timer_rlx

    def receiving_alert_timer_is_over(self):
        if self.countdown_timer_tempo.over:
            self.stop_all_if_tempo_is_over()
        elif self.countdown_timer_focus.over:
            self.stop_focus_start_rlx()
            self.countdown_timer_focus.over=False
            play_sound(Path(__file__).parent / 'sounds/descansar.mp3')
        elif self.countdown_timer_rlx.over:
            self.stop_rlx_start_focus()
            play_sound(Path(__file__).parent / 'sounds/trabalhar.mp3')

    def init_countdown_timer_tempo_focus_and_rlx(self):
        self.countdown_timer_rlx.running=False
        self.countdown_timer_tempo.running=True
        self.countdown_timer_focus.running=True
        self.current_state=self.states.FOCUS_TIME

    def play_or_pause_countdown_timer(self,value:bool):
        if not self.countdown_timer_tempo.over:
            if self.current_state== self.states.FOCUS_TIME:
                self.countdown_timer_focus.change_state(value)
            else:
                self.countdown_timer_rlx.change_state(value)    
            self.countdown_timer_tempo.change_state(value)
        
class ButtonStartHomePage(ft.UserControl):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page=page

    async def go_to_action_page(self,e):
        
        all_data["tempo_hrs"]=int(tempo_hrs_ref.current.value)
        all_data["tempo_min"]=int(tempo_min_ref.current.value)
        # all_data["tempo_seg"]=int(tempo_seg_ref.current.value)
        
        all_data["foco_min"]=int(foco_min_ref.current.value)

        all_data["rlx_min"]=int(rlx_min_ref.current.value)

        await self.page.clean_async()
        await action_page(self.page)

    def build(self):
        self.button=ft.ElevatedButton(content=ft.Text("start",size=30),on_click=self.go_to_action_page,)
        return self.button
    
class ReturnHomePageButton(ft.UserControl):
    def __init__(self,page:ft.Page):
        super().__init__()
        self.page=page

    def build(self):
        self.button = ft.IconButton(icon=ft.icons.ARROW_BACK,on_click=self.go_to_home_page)
        return self.button

    async def go_to_home_page(self,e):
        await self.page.clean_async()
        await home_page(self.page)

    

ft.app(target=main)