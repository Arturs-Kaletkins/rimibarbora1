import heapq #darbs ar prioritāti
import time #darbs ar pauzi sleep
import re #filtrēšana pēc koda vārdiem
from selenium import webdriver #vadības import lai izmantotu selenium
from selenium.webdriver.edge.service import Service #ļauj izveidot service for Edge
from selenium.webdriver.common.by import By #importē elementu meklēšanai
from selenium.webdriver.support.ui import WebDriverWait #gaidīšana kad paradīsies produkts
from selenium.webdriver.support import expected_conditions as EC #gaidīšana kad produkts ir redzams
from webdriver_manager.microsoft import EdgeChromiumDriverManager #ļauj automātiski lejupielādēt un instalēt Edge WebDriver

#veidojam darbu ar Edge
def setup_driver(): #izveido Edge
    options = webdriver.EdgeOptions() #iestata parlukprogrammas iestatijumus
    options.add_argument('--disable-gpu') #izsledz GPU paatrinajumu lai optimizetu
    service = Service(EdgeChromiumDriverManager().install()) #instale Edge
    return webdriver.Edge(service=service, options=options) #atver Edge parluku

#parluko lapi lidz lejai lidz ta ir pilniba ieladeta