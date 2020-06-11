from chromepy.remote import ChromeRemote


remote = ChromeRemote()
print('remote url', remote.current_url)

remote.get_screenshot_as_file('teste.png')