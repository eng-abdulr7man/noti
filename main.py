"""
Simple Notification Logger
Clean, Simple, Working Perfectly
"""

import os
import json
import random
from datetime import datetime, timedelta
from collections import Counter

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import MDSnackbar

# ============================================================================
# SIMPLE CLEAN KV DESIGN
# ============================================================================

KV = '''
<NotificationCard>:
    size_hint_y: None
    height: dp(110)
    padding: dp(15)
    spacing: dp(10)
    elevation: 1
    radius: [12]
    md_bg_color: 1, 1, 1, 1
    
    MDBoxLayout:
        orientation: 'horizontal'
        spacing: dp(12)
        
        # Simple icon circle
        MDBoxLayout:
            size_hint: None, None
            size: dp(45), dp(45)
            radius: [23]
            md_bg_color: root.icon_color
            
            MDLabel:
                text: root.icon_text
                font_size: '18sp'
                bold: True
                halign: 'center'
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
        
        # Text content
        MDBoxLayout:
            orientation: 'vertical'
            spacing: dp(4)
            
            # App name and time
            MDBoxLayout:
                orientation: 'horizontal'
                adaptive_height: True
                spacing: dp(8)
                
                MDLabel:
                    text: root.app_name
                    font_size: '15sp'
                    bold: True
                    theme_text_color: 'Primary'
                    size_hint_x: 0.6
                    shorten: True
                
                MDLabel:
                    text: root.time_text
                    font_size: '11sp'
                    theme_text_color: 'Hint'
                    size_hint_x: 0.4
                    halign: 'right'
            
            # Title
            MDLabel:
                text: root.title_text
                font_size: '13sp'
                theme_text_color: 'Primary'
                size_hint_y: None
                height: dp(20)
                max_lines: 1
                shorten: True
            
            # Message
            MDLabel:
                text: root.body_text
                font_size: '12sp'
                theme_text_color: 'Secondary'
                size_hint_y: None
                height: dp(18)
                max_lines: 1
                shorten: True


<MainScreen>:
    md_bg_color: 0.96, 0.96, 0.96, 1
    
    MDBoxLayout:
        orientation: 'vertical'
        
        # Simple header
        MDBoxLayout:
            size_hint_y: None
            height: dp(55)
            padding: dp(15), dp(10)
            md_bg_color: 0.1, 0.45, 0.8, 1
            
            MDLabel:
                text: 'Notification Logger'
                font_size: '20sp'
                bold: True
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
                size_hint_x: 0.8
            
            MDLabel:
                id: count_label
                text: '0'
                font_size: '20sp'
                bold: True
                theme_text_color: 'Custom'
                text_color: 1, 1, 1, 1
                halign: 'right'
                size_hint_x: 0.2
        
        # Content area
        MDScrollView:
            MDBoxLayout:
                orientation: 'vertical'
                padding: dp(12)
                spacing: dp(8)
                adaptive_height: True
                
                # Search
                MDTextField:
                    id: search_field
                    hint_text: 'Search...'
                    mode: 'rectangle'
                    radius: [8]
                    size_hint_y: None
                    height: dp(45)
                    on_text: root.on_search(self.text)
                
                # Simple buttons
                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(8)
                    
                    MDRaisedButton:
                        text: 'REFRESH'
                        size_hint_x: 0.5
                        md_bg_color: 0.1, 0.45, 0.8, 1
                        on_release: root.load_notifications()
                    
                    MDRaisedButton:
                        text: 'CLEAR ALL'
                        size_hint_x: 0.5
                        md_bg_color: 0.8, 0.2, 0.2, 1
                        on_release: root.confirm_clear()
                
                # Stats
                MDBoxLayout:
                    adaptive_height: True
                    spacing: dp(8)
                    padding: [0, dp(5)]
                    
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(65)
                        padding: dp(10)
                        elevation: 1
                        radius: [8]
                        
                        MDLabel:
                            text: root.total_text
                            font_size: '18sp'
                            bold: True
                            halign: 'center'
                            theme_text_color: 'Primary'
                        
                        MDLabel:
                            text: 'Total'
                            font_size: '10sp'
                            halign: 'center'
                            theme_text_color: 'Hint'
                    
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(65)
                        padding: dp(10)
                        elevation: 1
                        radius: [8]
                        
                        MDLabel:
                            text: root.today_text
                            font_size: '18sp'
                            bold: True
                            halign: 'center'
                            theme_text_color: 'Primary'
                        
                        MDLabel:
                            text: 'Today'
                            font_size: '10sp'
                            halign: 'center'
                            theme_text_color: 'Hint'
                    
                    MDCard:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: dp(65)
                        padding: dp(10)
                        elevation: 1
                        radius: [8]
                        
                        MDLabel:
                            text: root.apps_text
                            font_size: '18sp'
                            bold: True
                            halign: 'center'
                            theme_text_color: 'Primary'
                        
                        MDLabel:
                            text: 'Apps'
                            font_size: '10sp'
                            halign: 'center'
                            theme_text_color: 'Hint'
                
                # Notifications list
                MDBoxLayout:
                    id: notifications_list
                    orientation: 'vertical'
                    spacing: dp(8)
                    adaptive_height: True
                    padding: [0, dp(60), 0, 0]
        
        # Add button at bottom
        MDRaisedButton:
            text: '+ ADD TEST NOTIFICATION'
            size_hint_y: None
            height: dp(50)
            md_bg_color: 0.18, 0.7, 0.3, 1
            pos_hint: {'center_x': 0.5}
            on_release: root.add_test_notification()
            font_size: '14sp'
            bold: True
'''


# ============================================================================
# SIMPLE NOTIFICATION CARD
# ============================================================================

class NotificationCard(MDCard):
    """Simple clean notification card"""
    
    app_name = StringProperty('')
    title_text = StringProperty('')
    body_text = StringProperty('')
    time_text = StringProperty('')
    icon_text = StringProperty('A')
    icon_color = [0.1, 0.45, 0.8, 1]
    
    def __init__(self, notification_data, **kwargs):
        super().__init__(**kwargs)
        
        app_name = notification_data.get('app_name', 'Unknown')
        title = notification_data.get('title', '')
        text = notification_data.get('text', '')
        timestamp = notification_data.get('timestamp', '')
        
        # Simple time format
        try:
            dt = datetime.fromisoformat(timestamp)
            now = datetime.now()
            
            if dt.date() == now.date():
                time_str = dt.strftime('%I:%M %p')
            elif dt.date() == (now - timedelta(days=1)).date():
                time_str = 'Yesterday'
            else:
                time_str = dt.strftime('%b %d')
        except:
            time_str = ''
        
        # Get app color
        colors = {
            'whatsapp': [0.07, 0.47, 0.33, 1],
            'gmail': [0.77, 0.13, 0.12, 1],
            'facebook': [0.09, 0.46, 0.95, 1],
            'instagram': [0.75, 0.21, 0.37, 1],
            'telegram': [0, 0.53, 0.8, 1],
            'youtube': [0.8, 0, 0, 1],
        }
        
        for key, color in colors.items():
            if key in app_name.lower():
                self.icon_color = color
                break
        
        # Set simple properties
        self.app_name = app_name[:20]
        self.title_text = title[:50] if title else ''
        self.body_text = text[:80] if text else ''
        self.time_text = time_str
        self.icon_text = app_name[0].upper() if app_name else 'A'


# ============================================================================
# MAIN SCREEN
# ============================================================================

class MainScreen(Screen):
    """Simple main screen"""
    
    total_text = StringProperty('0')
    today_text = StringProperty('0')
    apps_text = StringProperty('0')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.search_timer = None
    
    def on_enter(self):
        Clock.schedule_once(lambda dt: self.load_notifications(), 0.1)
    
    def on_search(self, text):
        """Search with small delay"""
        if self.search_timer:
            self.search_timer.cancel()
        self.search_timer = Clock.schedule_once(lambda dt: self.load_notifications(), 0.3)
    
    def load_notifications(self):
        """Load notifications"""
        notifications_list = self.ids.notifications_list
        notifications_list.clear_widgets()
        
        # Load data
        notifications = []
        if os.path.exists('notifications.json'):
            try:
                with open('notifications.json', 'r', encoding='utf-8') as f:
                    notifications = json.load(f)
            except:
                pass
        
        # Sort by newest
        notifications.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
        # Search filter
        search_text = self.ids.search_field.text.strip().lower()
        filtered = []
        
        if search_text:
            for n in notifications:
                if (search_text in n.get('app_name', '').lower() or
                    search_text in n.get('title', '').lower() or
                    search_text in n.get('text', '').lower()):
                    filtered.append(n)
        else:
            filtered = notifications
        
        # Update stats
        total = len(filtered)
        today = sum(1 for n in filtered if self._is_today(n.get('timestamp', '')))
        apps = len(set(n.get('app_name', '') for n in filtered))
        
        self.total_text = str(total)
        self.today_text = str(today)
        self.apps_text = str(apps)
        self.ids.count_label.text = str(total)
        
        # Show notifications
        if not filtered:
            empty = MDLabel(
                text='No notifications\n\nTap ADD button below',
                halign='center',
                theme_text_color='Hint',
                font_size='14sp',
                size_hint_y=None,
                height=dp(100)
            )
            notifications_list.add_widget(empty)
        else:
            for notif in filtered[:50]:
                card = NotificationCard(notif)
                notifications_list.add_widget(card)
    
    def _is_today(self, timestamp):
        try:
            return datetime.fromisoformat(timestamp).date() == datetime.now().date()
        except:
            return False
    
    def confirm_clear(self):
        """Confirm before clearing"""
        dialog = MDDialog(
            title='Clear All?',
            text='Delete all notifications?',
            buttons=[
                MDFlatButton(text='CANCEL', on_release=lambda x: dialog.dismiss()),
                MDFlatButton(text='DELETE', on_release=lambda x: self._clear_all(dialog)),
            ],
        )
        dialog.open()
    
    def _clear_all(self, dialog):
        """Clear all notifications"""
        if os.path.exists('notifications.json'):
            os.remove('notifications.json')
        dialog.dismiss()
        self.load_notifications()
        self._show_snackbar('Cleared')
    
    def add_test_notification(self):
        """Add test notification"""
        test_data = [
            {
                'app_name': 'WhatsApp',
                'title': 'New message from Sarah',
                'text': 'Hey! Are we still on for dinner tonight?',
                'timestamp': datetime.now().isoformat()
            },
            {
                'app_name': 'Gmail',
                'title': 'Meeting reminder',
                'text': 'Team standup in 30 minutes',
                'timestamp': datetime.now().isoformat()
            },
            {
                'app_name': 'Instagram',
                'title': 'New follower',
                'text': 'john_doe started following you',
                'timestamp': (datetime.now() - timedelta(hours=2)).isoformat()
            },
            {
                'app_name': 'YouTube',
                'title': 'New video uploaded',
                'text': 'Best Smartphones 2024 Review',
                'timestamp': (datetime.now() - timedelta(hours=5)).isoformat()
            },
            {
                'app_name': 'Facebook',
                'title': 'Event invitation',
                'text': 'Tech Meetup 2024 next weekend',
                'timestamp': (datetime.now() - timedelta(days=1)).isoformat()
            },
        ]
        
        new_notification = random.choice(test_data)
        
        notifications = []
        if os.path.exists('notifications.json'):
            try:
                with open('notifications.json', 'r', encoding='utf-8') as f:
                    notifications = json.load(f)
            except:
                pass
        
        notifications.insert(0, new_notification)
        
        if len(notifications) > 200:
            notifications = notifications[:200]
        
        with open('notifications.json', 'w', encoding='utf-8') as f:
            json.dump(notifications, f, ensure_ascii=False, indent=2)
        
        self.load_notifications()
        self._show_snackbar(f'Added: {new_notification["app_name"]}')
    
    def _show_snackbar(self, text):
        """Show simple snackbar"""
        try:
            snackbar = MDSnackbar(
                MDLabel(text=text, theme_text_color='Custom', text_color=(1, 1, 1, 1)),
                duration=2,
            )
            snackbar.open()
        except:
            pass


# ============================================================================
# SIMPLE APP
# ============================================================================

class NotificationLoggerApp(MDApp):
    """Simple application"""
    
    def build(self):
        Window.size = (420, 750)
        Window.minimum_width = 350
        Window.minimum_height = 600
        
        self.theme_cls.primary_palette = 'Blue'
        self.theme_cls.theme_style = 'Light'
        
        Builder.load_string(KV)
        
        return MainScreen()


if __name__ == '__main__':
    NotificationLoggerApp().run()