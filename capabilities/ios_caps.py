import os

app = os.path.join(os.path.dirname(__file__), '../apps/ios/UIKitCatalog', 'UIKitCatalog-iphonesimulator.zip')
app = os.path.abspath(app)

ios_caps = {
                'app': app,
                'platformName': 'iOS',
                'deviceName': 'iPhone 11',
                'platformVersion': '13.7',
                'automationName': 'XCUITest',
                'noReset': 'true',
                'isHeadless': 'true'
}