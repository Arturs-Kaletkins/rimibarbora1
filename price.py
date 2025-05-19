import heapq #darbs ar prioritāti
import time #darbs ar pauzi sleep
import re #filtrēšana pēc koda vārdiem
from selenium import webdriver #vadības import lai izmantotu selenium
from selenium.webdriver.edge.service import Service #ļauj izveidot service for Edge
from selenium.webdriver.common.by import By #importē elementu meklēšanai
from selenium.webdriver.support.ui import WebDriverWait #gaidīšana kad paradīsies produkts
from selenium.webdriver.support import expected_conditions as EC #gaidīšana kad produkts ir redzams būs zēm EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager #ļauj automātiski lejupielādēt un instalēt Edge WebDriver

#veidojam darbu ar Edge
def setup_driver(): #izveido Edge
    options = webdriver.EdgeOptions() #iestata parlukprogrammas iestatijumus
    options.add_argument('--disable-gpu') #izsledz GPU paatrinajumu lai optimizetu
    service = Service(EdgeChromiumDriverManager().install()) #instale Edge
    return webdriver.Edge(service=service, options=options) #atver Edge parluku

#parluko lapi lidz lejai lidz ta ir pilniba ieladeta
def pages(driver): #scrollē lapu
    last = driver.execute_script("return document.body.scrollHeight") #saglabā lapas augstumu
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") #pārvieto lapu uz leju
        time.sleep(1) #gaida 1 sekundi
        new = driver.execute_script("return document.body.scrollHeight") #saglabā jauno augstumu
        if new == last: #ja jaunais augstums ir vienāds ar iepriekšējo augstumu
            break #beidz scrollēt
        last = new #saglabā jauno augstumu

#meklē preces Rimi veikalā
def search_rimi(driver, query, keyword=None): #meklē preces rimi
    # veido Rimi URL lai mekletu pec nosaukuma
    url = f"https://www.rimi.lv/e-veikals/lv/meklesana?currentPage=1&pageSize=80&query={query}%3Aprice-asc%3AassortmentStatus%3AinAssortment"
    driver.get(url) #atver lapu
    pages(driver) #pārlūko lapu līdz lejai

    # gaida kad preces ieladēsies
    try:
        WebDriverWait(driver, 25).until( #gaida 25 sekundes līdz preces ielādējas
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.product-grid__item")) #gaida līdz preces ir redzamas
        )
        items = driver.find_elements(By.CSS_SELECTOR, "li.product-grid__item") #atrod visas preces
    except: #ja preces nav atrastas
        print("Rimi: prece netika atrasta") #izvada kļūdu
        return []

    #ja preces ir atrastas meklējam nosaukumu un cenu
    results = []
    for item in items: #iziet cauri visām precēm
        try:
            name = item.find_element(By.CSS_SELECTOR, "p.card__name").text.strip() #atrod nosaukumu

            #pārbauda vai atslēgvārds kā atsevišķs vārds ir produkta nosaukumā, ja nē tad ignorējam
            if keyword and not re.search(rf"\b{re.escape(keyword)}\b", name, re.IGNORECASE):
                continue

            #ja nosaukums satur meklēto vārdu tad meklējam cenu
            scanner = item.find_element(By.CSS_SELECTOR, "div.card__price-wrapper") #atrod euro cenu
            ever = scanner.find_element(By.CSS_SELECTOR, "span").text.strip() #atrod veselo daļu

            part = '' #saglabājam daļu
            #ja cena satur centus tad meklējam tos
            try:
                part = scanner.find_element(By.CSS_SELECTOR, "sup").text.strip() #atrod centus
            except:
                pass #ja nav centu tad ignorējam
            #ja cena satur centus tad pievienojam tos
            if part:
                price = float(f"{ever}.{part}") #pievienojam centus
            else:
                price = float(ever.replace(",", ".")) #ja nav centu tad pievienojam veselo daļu
                #izvada rezultātus
            results.append(("Rimi", name, price))
        except:
            continue
    return results

#meklē preces Barbora veikalā
def search_barbora(driver, query): #meklē preces barbora
    url = f"https://barbora.lv/meklet?q={query}" #veido URL lai mekletu pec nosaukuma
    driver.get(url) #atver lapu

    
    #gaida kad preces ieladēsies
    try:
        WebDriverWait(driver, 25).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li[data-testid^='product-card']"))
        ) #gaida līdz preces ir redzamas
        items = driver.find_elements(By.CSS_SELECTOR, "li[data-testid^='product-card']") #atrod visas preces
        
    except: #ja preces nav atrastas
        print("Barbora: prece netika atrasta") #izvada kļūdu
        return [] #izvada tukšo sarakstu

    results = [] #veidosim sarakstu ar precem
    
    for item in items: #ņēmam atrastas preces pa vienai 
        try:
            name = item.find_element(By.CSS_SELECTOR, "a.tw-break-words").text.strip() #atrod nosaukumu
            
            #pārbauda ja nosaukums nav tukšs un name nav atrasts tas nosaukums, tad izlaižam to
            if query and not re.search(rf"\b{re.escape(query)}\b", name, re.IGNORECASE):
                continue #izlaižam un turpinam
                
            meta = item.find_element(By.CSS_SELECTOR, "meta[itemprop='price']") #atrod kur glabajas cena vietnē
            price = float(meta.get_attribute("content").replace(",", ".")) #meklejam cenu zem content un rediģējam
            results.append(("Barbora", name, price)) #izvada rezultātus
        except:
            continue #ja precei nav cenas tad turpinam
    return results #izmanto rezultātus tālāk

#meklē lētāko preci
def cheap(products): #funkcija meklē lētāko preci
    driver = setup_driver() #startē brauzeri
    #izveido meklēšanas vaicājumu
    try:
        rimi_results = search_rimi(driver, products, keyword=products) #meklē preces Rimi veikalā
        barbora_results = search_barbora(driver, products) #meklē preces Barbora veikalā

        all_results = rimi_results + barbora_results #apvieno rezultātus
        if not all_results: #ja nav atrastas preces tad izvada kļūdu
            print("Prece netika atrasta nevienā veikalā")
            return

        heap = [(price, store, name) for store, name, price in all_results] #izveido kaudzi ar rezultātiem lai atri atrastu lētāko
        heapq.heapify(heap)

        minim = heapq.nsmallest(1, heap)[0][0] #atrod lētāko cenu
        cheaper = [item for item in heap if item[0] == minim] #atrod lētāko preci
        stores = set(item[1] for item in cheaper) #izveido veikalu sarakstu kur cena ir vienāda ar minimalo
#izvada sarakstu ar visām precēm
        print(f"\nAtrastās preces: {len(all_results)}")
        for price, store, name in sorted(heap):
            print(f"{store}: {name} - {price:.2f} €") #izvada rezultātus

        #izvada rezultatu par lētāko cenu vai par to ka ta ir vienāda abos veikalos
        if len(stores) > 1:
            print(f"\nCena precei «{products}» ir vienāda: {minim:.2f} € veikalos {', '.join(stores)}")
        else:
            cheapest = cheaper[0]
            print(f"\nVislētākā prece: {cheapest[2]}")
            print(f"Cena: {cheapest[0]:.2f} € veikalā {cheapest[1]}")
    #aizver brauzeri
    finally:
        driver.quit()
#ja skripts tiek palaists no komandas rindas tad jautājam nosaukumu
if _name_ == "_main_":
    query = input("Ievadiet preces nosaukumu: ")
    cheap(query) #meklē lētāko preci
