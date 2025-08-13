from selenium import webdriver
from axe_selenium_python import Axe
from datetime import datetime


def writeTxt(results):
    txt = ""
    for violation in results["violations"]:
        text = """
網址: {webUrl}
問題: {description}
嚴重性: {impact}
影響元素: {html}
修復建議: {helpUrl}
--------------------------------------------------
"""
        txt = txt + text.format(webUrl=_webUrl,
                                description=violation['description'],
                                impact=violation['impact'],
                                html=violation['nodes'][0]['html'].replace(
                                    "\"", "'"),
                                helpUrl=violation['helpUrl'])

    f = open(_date_time_string + ".txt", "a", encoding="UTF-8")

    f.write(txt)


def test_web_url(webUrl):

    global _webUrl
    _webUrl = webUrl

    # driver = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Firefox()
    driver.get(webUrl)
    axe = Axe(driver)

    # Inject axe-core javascript into page.
    axe.inject()

    # Run axe accessibility checks.
    results = axe.run()

    # Write results to file
    writeTxt(results)

    # axe.write_results(results, 'a11y.json')
    axe.write_results(results["violations"], _date_time_string + ".json")
    driver.close()

    # Assert no violations are found
    # assert len(results["violations"]) == 0, axe.report(results["violations"])


def Test():    

    now = datetime.now()
    global _date_time_string
    _date_time_string = now.strftime("%Y%m%d%H%M%S")

    f = open('list.txt')
    for line in f.readlines():
         print(line)
         test_web_url(line)

    f.close

Test()