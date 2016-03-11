# Selenium
## Switch to activated tab page
Neither make sense.... ╮(╯﹏╰）╭)
1. Try using ShortCuts (CONTROL + TAB), or (COMMAND + TAB) instead
`self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)`
`WebDriverException: unknown error: cannot focus element`
1. Try using ActionChains
actions = ActionChains(self.driver)      
actions.key_down(Keys.CONTROL).key_down(Keys.TAB).key_up(Keys.TAB).key_up(Keys.CONTROL).perform()