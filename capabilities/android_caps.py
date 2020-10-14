import os

app = os.path.join(os.path.dirname(__file__),
                           '../apps/Android/',
                           'ApiDemos-debug.apk')
app = os.path.abspath(app)

android_caps={
                'app': app,
                'platformName': 'Android',
                'platformVersion': '11.0',
                'deviceName': 'emulator-5554',
                'automationName': 'UiAutomator2',
                'uiautomator2ServerInstallTimeout': '60000',
                'noReset': 'true',
                'isHeadless': 'true'
}