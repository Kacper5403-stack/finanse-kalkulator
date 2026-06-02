import streamlit as st
import re

st.set_page_config(page_title="Asystent - Finanse Międzynarodowe", layout="wide")

# Podpis w lewym górnym rogu
st.sidebar.success("Narzędzie zostało stworzone przez:\n**Kacper Żywczak 195477**")
st.sidebar.markdown("---")

# Menu boczne (zamiast listy rozwijanej mamy zawsze widoczne pozycje / kafelki)
st.sidebar.markdown("### Wybierz moduł do obliczeń:")
opcja = st.sidebar.radio(
    "", # Puste etykiety, żeby było czysto
    ["1. Odwracanie kursów", 
     "2. Kursy krzyżowe (Bid/Ask)", 
     "3. Kontrakty FRA (Pojedyncza transakcja)",
     "4. Portfel FRA (Złożona strategia)",
     "5. Kontrakty Forward (Zabezpieczenie walutowe)",
     "6. Hedging Krzyżowy (Cross-Hedging)",
     "7. Forwardy Towarowe i Ryzyko Bazy",
     "8. Emisja Obligacji i Lokaty (Strip FRA)",
     "9. Wyszukiwarka Teorii (Baza Wiedzy)"]
)

st.title("🌍 Kalkulator Zadań: Finanse Międzynarodowe")
st.markdown("Wypełniaj pola od lewej do prawej. Aplikacja automatycznie dobierze odpowiednie pozycje rynkowe.")
st.markdown("---")

# --------------------------------------------------------------------------------
# MODUŁ 1: ODWRACANIE KURSÓW
# --------------------------------------------------------------------------------
if opcja == "1. Odwracanie kursów":
    st.header("🔄 Odwracanie kursów walutowych")
    
    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "Spójrz na treść zadania. Jeśli masz podany kurs w formacie `A/B`, a każą znaleźć `B/A` (np. masz USD/PLN, a szukasz PLN/USD):\n"
            "1. Jako 'Walutę bazową' wpisz pierwszą walutę z zadania (np. USD).\n"
            "2. Jako 'Walutę kwotowaną' wpisz drugą walutę (np. PLN).\n"
            "3. Pierwsza kwota w zadaniu to najczęściej mniejsza cyfra (Kupno/Bid), druga to większa (Sprzedaż/Ask). Wpisz je poniżej.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        waluta_bazowa = st.text_input("Pierwsza waluta z zadania (bazowa)", "USD")
    with col2:
        waluta_kwotowana = st.text_input("Druga waluta z zadania (kwotowana)", "PLN")
        
    col4, col5 = st.columns(2)
    with col4:
        kurs_bid = st.number_input("Wpisz niższy kurs (Bid / Kupno)", value=3.6480, format="%.4f", step=0.0001)
    with col5:
        kurs_ask = st.number_input("Wpisz wyższy kurs (Ask / Sprzedaż)", value=3.7828, format="%.4f", step=0.0001)

    if st.button("Wylicz nowy kurs"):
        odwrotny_bid = 1 / kurs_ask
        odwrotny_ask = 1 / kurs_bid
        
        st.success(f"**Gotowy wynik:** Odwrócony kurs {waluta_kwotowana}/{waluta_bazowa} wynosi **{odwrotny_bid:.4f} - {odwrotny_ask:.4f}**")
        
        st.subheader("Rozpisanie na kartkę:")
        st.latex(rf"Bid_{{{waluta_kwotowana}/{waluta_bazowa}}} = \frac{{1}}{{Ask_{{{waluta_bazowa}/{waluta_kwotowana}}}}} = \frac{{1}}{{{kurs_ask}}} = {odwrotny_bid:.4f}")
        st.latex(rf"Ask_{{{waluta_kwotowana}/{waluta_bazowa}}} = \frac{{1}}{{Bid_{{{waluta_bazowa}/{waluta_kwotowana}}}}} = \frac{{1}}{{{kurs_bid}}} = {odwrotny_ask:.4f}")

# --------------------------------------------------------------------------------
# MODUŁ 2: KURSY KRZYŻOWE
# --------------------------------------------------------------------------------
elif opcja == "2. Kursy krzyżowe (Bid/Ask)":
    st.header("✖️ Wyznaczanie kursów krzyżowych")
    
    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "W zadaniach na kursy krzyżowe zawsze masz dwie pary, które mają **jedną walutę wspólną**. Zobacz, gdzie ona stoi w obu kursach:\n"
            "- Jeśli waluta wspólna w jednym kursie jest Z PRZODU, a w drugim Z TYŁU (np. `GBP`/USD i USD/`CHF`) ➔ Wybierz **Mnożenie**.\n"
            "- Jeśli waluta wspólna w OBU kursach jest Z PRZODU (np. `EUR`/USD i `EUR`/GBP) ➔ Wybierz **Dzielenie (wspólna bazowa)**.\n"
            "- Jeśli waluta wspólna w OBU kursach jest Z TYŁU (np. USD/`PLN` i EUR/`PLN`) ➔ Wybierz **Dzielenie (wspólna kwotowana)**.")
    
    typ_równania = st.radio(
        "Zaznacz odpowiedni schemat z instrukcji powyżej:",
        ["Mnożenie: Mamy A/X oraz X/B -> Szukamy A/B", 
         "Dzielenie (wspólna bazowa): Mamy X/A oraz X/B -> Szukamy A/B",
         "Dzielenie (wspólna kwotowana): Mamy A/X oraz B/X -> Szukamy A/B"]
    )
    
    st.markdown("---")
    
    if typ_równania == "Dzielenie (wspólna bazowa): Mamy X/A oraz X/B -> Szukamy A/B":
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Para 1**")
            para1_nazwa = st.text_input("Nazwa pierwszej pary (np. EUR/USD)", "EUR/USD")
            p1_bid = st.number_input("Pierwszy (niższy) kurs Pary 1", value=1.1577, format="%.4f", step=0.0001)
            p1_ask = st.number_input("Drugi (wyższy) kurs Pary 1", value=1.1578, format="%.4f", step=0.0001)
        with c2:
            st.write("**Para 2**")
            para2_nazwa = st.text_input("Nazwa drugiej pary (np. EUR/GBP)", "EUR/GBP")
            p2_bid = st.number_input("Pierwszy (niższy) kurs Pary 2", value=0.8402, format="%.4f", step=0.0001)
            p2_ask = st.number_input("Drugi (wyższy) kurs Pary 2", value=0.8405, format="%.4f", step=0.0001)
            
        if st.button("Pokaż wynik krzyżowy"):
            wynik_bid = p1_bid / p2_ask
            wynik_ask = p1_ask / p2_bid
            st.success(f"**Gotowy wynik:** {wynik_bid:.4f} - {wynik_ask:.4f}")
            st.latex(rf"Bid = \frac{{Bid_{{{para1_nazwa}}}}}{{Ask_{{{para2_nazwa}}}}} = \frac{{{p1_bid}}}{{{p2_ask}}} = {wynik_bid:.4f}")
            st.latex(rf"Ask = \frac{{Ask_{{{para1_nazwa}}}}}{{Bid_{{{para2_nazwa}}}}} = \frac{{{p1_ask}}}{{{p2_bid}}} = {wynik_ask:.4f}")

    elif typ_równania == "Mnożenie: Mamy A/X oraz X/B -> Szukamy A/B":
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Para 1**")
            p1_bid = st.number_input("Niższy kurs Pary 1", value=1.3560, format="%.4f", step=0.0001)
            p1_ask = st.number_input("Wyższy kurs Pary 1", value=1.3565, format="%.4f", step=0.0001)
        with c2:
            st.write("**Para 2**")
            p2_bid = st.number_input("Niższy kurs Pary 2", value=1.0615, format="%.4f", step=0.0001)
            p2_ask = st.number_input("Wyższy kurs Pary 2", value=1.0620, format="%.4f", step=0.0001)
            
        if st.button("Pokaż wynik krzyżowy"):
            wynik_bid = p1_bid * p2_bid
            wynik_ask = p1_ask * p2_ask
            st.success(f"**Gotowy wynik:** {wynik_bid:.4f} - {wynik_ask:.4f}")
            st.latex(rf"Bid = {p1_bid} \times {p2_bid} = {wynik_bid:.4f}")
            st.latex(rf"Ask = {p1_ask} \times {p2_ask} = {wynik_ask:.4f}")
            
    elif typ_równania == "Dzielenie (wspólna kwotowana): Mamy A/X oraz B/X -> Szukamy A/B":
        c1, c2 = st.columns(2)
        with c1:
            st.write("**Para 1 (ta która powinna być na górze w wyniku)**")
            p1_bid = st.number_input("Niższy kurs Pary 1", value=3.8000, format="%.4f", step=0.0001)
            p1_ask = st.number_input("Wyższy kurs Pary 1", value=3.8200, format="%.4f", step=0.0001)
        with c2:
            st.write("**Para 2 (ta która powinna być na dole)**")
            p2_bid = st.number_input("Niższy kurs Pary 2", value=4.5000, format="%.4f", step=0.0001)
            p2_ask = st.number_input("Wyższy kurs Pary 2", value=4.5200, format="%.4f", step=0.0001)
            
        if st.button("Pokaż wynik krzyżowy"):
            wynik_bid = p1_bid / p2_ask
            wynik_ask = p1_ask / p2_bid
            st.success(f"**Gotowy wynik:** {wynik_bid:.4f} - {wynik_ask:.4f}")
            st.latex(rf"Bid = \frac{{{p1_bid}}}{{{p2_ask}}} = {wynik_bid:.4f}")
            st.latex(rf"Ask = \frac{{{p1_ask}}}{{{p2_bid}}} = {wynik_ask:.4f}")

# --------------------------------------------------------------------------------
# MODUŁ 3: KONTRAKTY FRA (Pojedyncze)
# --------------------------------------------------------------------------------
elif opcja == "3. Kontrakty FRA (Pojedyncza transakcja)":
    st.header("🛡️ Zabezpieczanie stóp procentowych (FRA)")
    
    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "1. Co chce zrobić firma? Jeśli ma kasę ('ulokować nadwyżkę') ➔ wybierz **Lokata**. Jeśli chce pożyczyć ('zaciągnąć kredyt') ➔ wybierz **Kredyt**.\n"
            "2. W zadaniach o FRA pojawia się notacja np. **2x5**. Oznacza to, że transakcja ZACZYNA SIĘ za 2 miesiące, a TRWA 3 miesiące (bo 5 - 2 = 3). Wpisz odpowiednio start i czas trwania w pola poniżej.\n"
            "3. Przepisz kwotę, kursy FRA (Bid to mniejszy, Ask to większy) oraz prognozowany WIBOR z zadania.")

    c1, c2, c3 = st.columns(3)
    with c1:
        typ_ekspozycji = st.selectbox("Co robi firma w zadaniu?", ["Kredyt (Potrzebuje pieniędzy / Płaci odsetki)", "Lokata (Ma nadwyżkę / Dostaje odsetki)"])
        kwota = st.number_input("Kwota z zadania", value=15000000, step=100000)
    with c2:
        start_za = st.number_input("Start transakcji (za ile miesięcy?)", value=4, step=1)
        trwa = st.number_input("Czas trwania (ile miesięcy będzie trwać?)", value=6, step=1)
    with c3:
        marza = st.number_input("Czy zadanie podaje marżę banku? (Jeśli nie, zostaw 0)", value=1.80, step=0.01)
        
    st.markdown(f"> **Automatyczna podpowiedź:** Szukaj w tabelce kontraktu FRA o symbolu: **{start_za}X{start_za+trwa}**")
    
    st.markdown("---")
    c4, c5, c6 = st.columns(3)
    with c4:
        fra_bid = st.number_input("Niższy kurs FRA z tabeli (Bid w %)", value=5.128, step=0.001, format="%.3f")
    with c5:
        fra_ask = st.number_input("Wyższy kurs FRA z tabeli (Ask w %)", value=5.138, step=0.001, format="%.3f")
    with c6:
        wibor_rzeczywisty = st.number_input("Podany WIBOR w dniu uruchomienia (%)", value=6.15, step=0.01)

    if st.button("Pokaż jak rozliczyć to zadanie"):
        is_lokata = typ_ekspozycji == "Lokata (Ma nadwyżkę / Dostaje odsetki)"
        typ_fra = "SPRZEDAŻ kontraktu FRA (pozycja krótka na rynku)" if is_lokata else "KUPNO kontraktu FRA (pozycja długa na rynku)"
        kurs_fra = fra_bid if is_lokata else fra_ask
        uzasadnienie = "Spółka zabezpiecza się przed SPADKIEM stóp procentowych. Sprzedaż FRA 'zamraża' jej stały, wysoki zysk." if is_lokata else "Spółka zabezpiecza się przed WZROSTEM stóp procentowych. Kupno FRA 'zamraża' stały koszt kredytu, chroniąc przed podwyżkami."
        
        st.success(f"**Co musisz napisać na kolokwium (Wybór strategii):**\n\nNależy zawrzeć pozycję: **{typ_fra}**.\n\n**Dlaczego?** {uzasadnienie}\n**Zastosowany kurs (Cena FRA):** Używamy kursu {'Bid' if is_lokata else 'Ask'} wynoszącego **{kurs_fra}%**.")
        
        czas_ulamek = trwa / 12
        wibor_dec = wibor_rzeczywisty / 100
        fra_dec = kurs_fra / 100
        
        roznica = abs(wibor_dec - fra_dec)
        licznik = kwota * roznica * czas_ulamek
        mianownik = 1 + (wibor_dec * czas_ulamek)
        kwota_rozliczenia = licznik / mianownik
        
        if is_lokata:
            otrzyma_pieniadze = wibor_rzeczywisty < kurs_fra
            efektywna_stopa = kurs_fra + marza 
        else:
            otrzyma_pieniadze = wibor_rzeczywisty > kurs_fra
            efektywna_stopa = kurs_fra + marza

        wynik_tekst = f"Z rozliczenia FRA **Spółka OTRZYMA PŁATNOŚĆ** w wysokości **{kwota_rozliczenia:,.2f} PLN**" if otrzyma_pieniadze else f"Z rozliczenia FRA **Spółka MUSI ZAPŁACIĆ (dopłacić karę)** w kwocie **{kwota_rozliczenia:,.2f} PLN**"
        if wibor_rzeczywisty == kurs_fra:
            wynik_tekst = "**Kwota rozliczenia FRA wynosi 0 PLN**, ponieważ rynkowy WIBOR jest identyczny jak kurs FRA z dnia zawarcia."
            
        st.info(f"**Rozliczenie końcowe (Wypłata Settlement Amount):**\n\n{wynik_tekst}")
        st.markdown(f"**Efektywny koszt kredytu / zysk z lokaty wyniesie łącznie z marżą:** **{efektywna_stopa:.3f}%**")
        
        st.subheader("Rozpisanie wzoru (przepisz na kartkę):")
        st.latex(rf"\text{{Kwota}} = \frac{{{kwota:,.0f} \times |{wibor_dec:.4f} - {fra_dec:.4f}| \times \frac{{{trwa}}}{{12}}}}{{1 + {wibor_dec:.4f} \times \frac{{{trwa}}}{{12}}}} = {kwota_rozliczenia:,.2f} \text{{ PLN}}")

# --------------------------------------------------------------------------------
# MODUŁ 4: PORTFEL FRA 
# --------------------------------------------------------------------------------
elif opcja == "4. Portfel FRA (Złożona strategia)":
    st.header("🗂️ Złożona strategia (Portfel FRA)")
    
    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "To zadanie polega na tym, że firma/bank planuje KILKA różnych rzeczy na raz (np. 'za 3 miesiące klient wpłaci 25 mln', 'za 6 miesięcy ktoś weźmie kredyt na 40 mln'). \n"
            "Wpisz poniżej po kolei każde z takich wydarzeń w osobną linijkę (Transakcja 1, 2, 3).")
    
    st.subheader("Wypisz z zadania wszystkie zaplanowane działania:")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        typ1 = st.selectbox("Transakcja 1: Co się stanie?", ["Klient nam wpłaci (Lokata/Napływ)", "My pożyczamy (Kredyt/Wypływ)"], key="t1_typ")
    with col2:
        kwota1 = st.number_input("Ile milionów? (T1)", value=25.0, step=1.0, key="t1_k")
    with col3:
        start1 = st.number_input("Za ile miesięcy rusza? (T1)", value=3, step=1, key="t1_s")
    with col4:
        trwa1 = st.number_input("Na jaki czas? (T1)", value=6, step=1, key="t1_t")
        
    col5, col6, col7, col8 = st.columns(4)
    with col5:
        typ2 = st.selectbox("Transakcja 2: Co się stanie?", ["My pożyczamy (Kredyt/Wypływ)", "Klient nam wpłaci (Lokata/Napływ)"], key="t2_typ")
    with col6:
        kwota2 = st.number_input("Ile milionów? (T2)", value=40.0, step=1.0, key="t2_k")
    with col7:
        start2 = st.number_input("Za ile miesięcy rusza? (T2)", value=6, step=1, key="t2_s")
    with col8:
        trwa2 = st.number_input("Na jaki czas? (T2)", value=6, step=1, key="t2_t")

    col9, col10, col11, col12 = st.columns(4)
    with col9:
        typ3 = st.selectbox("Transakcja 3: Co się stanie?", ["My pożyczamy (Kredyt/Wypływ)", "Klient nam wpłaci (Lokata/Napływ)"], key="t3_typ")
    with col10:
        kwota3 = st.number_input("Ile milionów? (T3)", value=20.0, step=1.0, key="t3_k")
    with col11:
        start3 = st.number_input("Za ile miesięcy rusza? (T3)", value=9, step=1, key="t3_s")
    with col12:
        trwa3 = st.number_input("Na jaki czas? (T3)", value=3, step=1, key="t3_t")

    if st.button("Pokaż jak opisać cały portfel"):
        
        def opis_fra(typ, kwota, start, trwa):
            okres_koniec = start + trwa
            kontrakt = f"{start}X{okres_koniec}"
            if "Lokata" in typ:
                akcja = "SPRZEDAŻ kontraktu (Bid)"
                cel = "Ochrona przed spadkiem stóp procentowych z uwagi na długą pozycję w aktywach"
            else:
                akcja = "KUPNO kontraktu (Ask)"
                cel = "Ochrona przed wzrostem stóp procentowych z uwagi na pozycję w pasywach"
            return kontrakt, akcja, cel
            
        k1, a1, c1 = opis_fra(typ1, kwota1, start1, trwa1)
        k2, a2, c2 = opis_fra(typ2, kwota2, start2, trwa2)
        k3, a3, c3 = opis_fra(typ3, kwota3, start3, trwa3)
        
        st.success(f"**Co musisz napisać na kolokwium dla Transakcji 1:**\nBank musi użyć kontraktu **{k1}**. Właściwa decyzja to **{a1}** na nominał {kwota1} mln.\nUzasadnienie: *{c1}.*")
        st.success(f"**Co musisz napisać na kolokwium dla Transakcji 2:**\nBank musi użyć kontraktu **{k2}**. Właściwa decyzja to **{a2}** na nominał {kwota2} mln.\nUzasadnienie: *{c2}.*")
        st.success(f"**Co musisz napisać na kolokwium dla Transakcji 3:**\nBank musi użyć kontraktu **{k3}**. Właściwa decyzja to **{a3}** na nominał {kwota3} mln.\nUzasadnienie: *{c3}.*")

# --------------------------------------------------------------------------------
# MODUŁ 5: KONTRAKTY FORWARD
# --------------------------------------------------------------------------------
elif opcja == "5. Kontrakty Forward (Zabezpieczenie walutowe)":
    st.header("💱 Kontrakty Forward (Zabezpieczenie kursu)")
    
    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "1. Co kupuje/sprzedaje firma z zadania? \n"
            "- Ściąga towar z zagranicy (Import) i **Musi zapłacić** np. w USD? Zaznacz 'Import (płatność faktury)'.\n"
            "- Wysyła towar (Eksport) i **Dostanie pieniądze** np. w EUR? Zaznacz 'Eksport (wpływy z zewnątrz)'.\n"
            "2. Wpisz kwotę waluty, którą ma zapłacić/otrzymać.\n"
            "3. **UWAGA NA JPY (Jeny japońskie)!** Zaznacz ptaszka w polu obok, jeśli walutą z zadania są Jeny (ich kurs dzieli się przez 100).")

    c1, c2 = st.columns(2)
    with c1:
        rodzaj_transakcji = st.selectbox("Cel działania w zadaniu?", 
                                        ["Import (Firma ma dług / Płatność faktury w walucie)", 
                                         "Eksport (Firma zarobiła / Wpływ na konto w walucie)"])
        kwota_fx = st.number_input("Wpisz kwotę z zadania (w walucie obcej)", value=2400000, step=100000)
        mnoznik_jpy = st.checkbox("Zaznacz to, jeśli walutą w zadaniu są Jeny (JPY) lub kwotowanie jest za 100 jednostek")
    
    with c2:
        tryb_wprowadzania = st.radio("Jak zadanie podaje kursy rynkowe?", ["Są gotowe kursy (Bid/Ask) Forward podane na tacy", "Zadanie podaje kurs SPOT i oddzielnie Punkty Swap"])
        if tryb_wprowadzania == "Są gotowe kursy (Bid/Ask) Forward podane na tacy":
            kurs_fwd_bid = st.number_input("Niższy kurs Forward (Bid)", value=3.9425, format="%.4f", step=0.0001)
            kurs_fwd_ask = st.number_input("Wyższy kurs Forward (Ask)", value=3.9575, format="%.4f", step=0.0001)
        else:
            spot_bid = st.number_input("Niższy kurs Spot (Bid)", value=4.3320, format="%.4f", step=0.0001)
            spot_ask = st.number_input("Wyższy kurs Spot (Ask)", value=4.3320, format="%.4f", step=0.0001)
            swap = st.number_input("Punkty Swap z zadania (np. 0.0155)", value=0.0155, format="%.4f", step=0.0001)
            kurs_fwd_bid = spot_bid + swap
            kurs_fwd_ask = spot_ask + swap
            st.info(f"Program wyliczył bazowe kursy Forward dla Ciebie: Bid = {kurs_fwd_bid:.4f}, Ask = {kurs_fwd_ask:.4f}")
            
    if st.button("Pokaż rozliczenie zabezpieczenia"):
        is_import = "Import" in rodzaj_transakcji
        typ_fwd = "KUPNO kontraktu Forward po kursie wyższym (Ask)" if is_import else "SPRZEDAŻ kontraktu Forward po kursie niższym (Bid)"
        zastosowany_kurs = kurs_fwd_ask if is_import else kurs_fwd_bid
        
        dzielnik = 100 if mnoznik_jpy else 1
        kwota_pln = (kwota_fx / dzielnik) * zastosowany_kurs
        
        wyjasnienie = "Firma IMPORTOWA musi zapłacić fakturę dostawcy. Nie ma waluty, więc 'potrzebuje KUPIC walutę' na rynku Forward. Dostaje kurs gorszy z tabeli." if is_import else "Firma EKSPORTOWA dostanie zapłatę w walucie od zagranicznego klienta. Pieniądze wpłyną na konto, więc firma będzie chciała 'SPRZEDAĆ obcą walutę', wymieniając ją na złotówki."
        
        st.success(f"**Co pisać na kartkę (Strategia):** Należy dokonać operacji: **{typ_fwd}**.\n\n**Dlaczego?** {wyjasnienie}")
        st.info(f"Firma zagwarantowała sobie równowartość dokładnie **{kwota_pln:,.2f} PLN**")
        
        st.subheader("Wzór matematyczny do przepisania:")
        if mnoznik_jpy:
            st.latex(rf"\text{{Wartosc PLN}} = \frac{{{kwota_fx:,.0f}}}{{100}} \times {zastosowany_kurs:.4f} = {kwota_pln:,.2f} \text{{ PLN}}")
        else:
            st.latex(rf"\text{{Wartosc PLN}} = {kwota_fx:,.0f} \times {zastosowany_kurs:.4f} = {kwota_pln:,.2f} \text{{ PLN}}")

# --------------------------------------------------------------------------------
# MODUŁ 6: HEDGING KRZYŻOWY
# --------------------------------------------------------------------------------
elif opcja == "6. Hedging Krzyżowy (Cross-Hedging)":
    st.header("🔀 Hedging Krzyżowy (Cross-Hedging)")
    
    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "Zadania tego typu łatwo rozpoznać - firma ma zarobić/wydać walutę X, ale używa waluty Y do ubezpieczenia (bo waluta X nie jest notowana/ma złą płynność).\n"
            "1. **Waluta Target** (cel) – to ta główna, oryginalna z faktury (np. NOK, SEK, DKK z zadań skandynawskich).\n"
            "2. **Waluta Proxy** (ochrona) – to ta większa, stabilniejsza, używana zamiast właściwej (np. EUR).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**1. Prawdziwa waluta z faktury (Target)**")
        waluta_cel = st.text_input("Nazwa (np. NOK)", "NOK")
        kwota_cel = st.number_input("Pojemność faktury/ekspozycji", value=4800000, step=10000)
        spot_cel = st.number_input("Kurs dzisiejszy (Spot) dla tej waluty", value=0.3830, format="%.4f", step=0.0001)
        
    with col2:
        st.markdown("**2. Waluta użyta do ochrony (Proxy)**")
        waluta_proxy = st.text_input("Nazwa (np. EUR)", "EUR")
        spot_proxy = st.number_input("Kurs dzisiejszy (Spot) dla Proxy", value=4.3320, format="%.4f", step=0.0001)
        fwd_proxy = st.number_input("Niepotrzebny do tego wzoru, ale podany (Forward proxy)", value=4.3485, format="%.4f", step=0.0001)

    if st.button("Pokaż jak wyliczyć proporcję (Hedge Ratio)"):
        wartosc_pln = kwota_cel * spot_cel
        kwota_proxy = wartosc_pln / spot_proxy
        
        st.success(f"**Gotowy wynik na kartkę:** Aby wyrównać ryzyko z waluty {waluta_cel}, firma musi zabezpieczyć równe **{kwota_proxy:,.2f} {waluta_proxy}** na rynku Forward.")
        
        st.subheader("Dokładne rozpisanie na kolokwium:")
        st.latex(rf"\text{{Zastepczy Wolumen}}_{{{waluta_proxy}}} = \text{{Wolumen Faktury}}_{{{waluta_cel}}} \times \frac{{\text{{Spot}}_{{{waluta_cel}/PLN}}}}{{\text{{Spot}}_{{{waluta_proxy}/PLN}}}}")
        st.latex(rf"\text{{Zastepczy Wolumen}}_{{{waluta_proxy}}} = {kwota_cel:,.0f} \times \frac{{{spot_cel:.4f}}}{{{spot_proxy:.4f}}} = {kwota_proxy:,.2f}")

# --------------------------------------------------------------------------------
# MODUŁ 7: FORWARDY TOWAROWE
# --------------------------------------------------------------------------------
elif opcja == "7. Forwardy Towarowe i Ryzyko Bazy":
    st.header("🌾 Forwardy Towarowe (Ryzyko Bazy)")
    
    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "Czytasz treść o soi, rzepaku lub metalach. Problem: Ceny na polskim, lokalnym rynku różnią się od cen na wielkiej europejskiej giełdzie o jakiś procent.\n"
            "1. Jak firma to skupuje (produkcja), zaznacz 'Zakup (Kupno)'. Jak to rolnik/wydobywca – zaznacz 'Sprzedaż'.\n"
            "2. Najważniejszy haczyk: w zadaniu podane jest, że *'lokalne ceny są zazwyczaj o 2,5% niższe'*. Skoro są niższe, w rubryce 'Ryzyko Bazy' musisz bezwzględnie wpisać minus (np. `-2.5`).")
    
    col1, col2 = st.columns(2)
    with col1:
        kierunek = st.selectbox("Krok 1: Co firma robi z towarem?", ["Kupuje (Musi zabezpieczyć cenę zakupu - Ask)", "Sprzedaje (Musi uchronić zyski - Bid)"])
        wolumen = st.number_input("Ile kupują/sprzedają? (Np. 12000 ton)", value=12000.0, step=100.0)
    with col2:
        fwd_bid = st.number_input("Kurs giełdowy Niższy (Bid w EUR)", value=502.80, format="%.2f", step=0.1)
        fwd_ask = st.number_input("Kurs giełdowy Wyższy (Ask w EUR)", value=506.30, format="%.2f", step=0.1)
        
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    with col3:
        ryzyko_bazy = st.number_input("Wpisz procent odchylenia lokalnego (Ryzyko bazy). PAMIĘTAJ O MINUSIE jeśli jest niższe!", value=-2.50, step=0.1)
    with col4:
        fx_fwd = st.number_input("Dodatkowy kurs wymiany obcej waluty na polską (FX Forward)", value=4.3705, format="%.4f", step=0.0001)

    if st.button("Oblicz Koszty całego Surowca"):
        is_zakup = "Kupuje" in kierunek
        typ_fwd = "KUPNO kontraktu (Bierzemy wyższą cenę Ask z giełdy)" if is_zakup else "SPRZEDAŻ kontraktu (Bierzemy niższą cenę Bid)"
        kurs_surowca = fwd_ask if is_zakup else fwd_bid
        
        st.success(f"**Co musisz napisać (Krok 1 - Surowiec):** Firma musi wejść w operację **{typ_fwd}**. Kurs referencyjny wynosi {kurs_surowca:.2f}.")
        
        korekta_bazy_procentowa = ryzyko_bazy / 100
        efektywna_cena_waluta = kurs_surowca * (1 + korekta_bazy_procentowa)
        calkowita_wartosc_waluta = wolumen * efektywna_cena_waluta
        calkowita_wartosc_pln = calkowita_wartosc_waluta * fx_fwd
        
        st.info(f"**Co musisz napisać (Krok 2 - Korekta):** Po dodaniu korekty lokalnego podwórka ({ryzyko_bazy}%), zablokowana cena wyniesie **{efektywna_cena_waluta:.2f}** za tonę.")
        st.success(f"**Wynik Końcowy:** Za całość towaru zapłacą / zarobią dokładnie **{calkowita_wartosc_pln:,.2f} PLN** (po wymianie walut po kursie {fx_fwd:.4f}).")
        
        st.subheader("Wzory do przepisania na kolokwium:")
        st.latex(r"\text{Cena Efektywna} = \text{Forward}_{\text{Gielda}} \times (1 + \text{Ryzyko Bazy})")
        st.latex(rf"\text{{Cena Efektywna}} = {kurs_surowca:.2f} \times (1 + \frac{{{ryzyko_bazy}}}{{100}}) = {efektywna_cena_waluta:.2f}")
        st.latex(r"\text{Calosc PLN} = \text{Ile Ton} \times \text{Cena Efektywna} \times \text{Kurs Walut}")
        st.latex(rf"\text{{Calosc PLN}} = {wolumen:,.0f} \times {efektywna_cena_waluta:.2f} \times {fx_fwd:.4f} = {calkowita_wartosc_pln:,.2f}")

# --------------------------------------------------------------------------------
# MODUŁ 8: STRATEGIA KORPORACYJNA
# --------------------------------------------------------------------------------
elif opcja == "8. Emisja Obligacji i Lokaty (Strip FRA)":
    st.header("🏛️ Złożona Ekspozycja: Obligacje i Lokaty")
    
    st.info("💡 **Instrukcja (Krok po kroku):**\n"
            "Najtrudniejsze zadanie. Masz w nim informację, że firma wypuszcza Obligacje (tworzy dług na długi okres). Z drugiej strony firma ma pieniądze 'w nadwyżkach' i robi lokaty.\n"
            "1. 'Strip FRA' oznacza pocięcie długu na mniejsze kawałki. Jeżeli wypuszcza obligację za 2 miesiące, a okres odsetkowy trwa 3 miesiące, to zabezpiecza się serią: 2x5, 5x8, 8x11 itd. Program sam to wyliczy, wystarczy że podasz co ile miesięcy płacą odsetki (np. co 3 miesiące).\n"
            "2. Wpisz parametry poszczególnych małych lokat niżej.")

    st.subheader("1. Główny problem: Emisja Obligacji (Firma pożycza od inwestorów)")
    c1, c2, c3 = st.columns(3)
    with c1:
        kwota_obl = st.number_input("Ile milionów emitują?", value=100.0)
        marza_obl = st.number_input("Ile punktów dolicza bank? (Marża z zadania w %)", value=1.20, step=0.01)
    with c2:
        start_obl = st.number_input("Kiedy rusza emisja? (Za ile miesięcy)", value=2)
        okres_obl = st.number_input("Co ile miesięcy płacą z tego odsetki?", value=3)
    with c3:
        liczba_okresow = st.number_input("Ile takich rat opisujesz z zadania?", value=3, step=1, max_value=6)
        
    st.markdown("---")
    st.subheader("2. Poboczne transakcje: LOKATY (Firma ucieka w inwestycje)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Lokata 1**")
        l1_kwota = st.number_input("L1: Ile Milionów", value=30.0)
        l1_start = st.number_input("L1: Start za (miesięcy)", value=1)
        l1_trwa = st.number_input("L1: Trwa ile (miesięcy)", value=3)
    with col2:
        st.markdown("**Lokata 2**")
        l2_kwota = st.number_input("L2: Ile Milionów", value=25.0)
        l2_start = st.number_input("L2: Start za (miesięcy)", value=4)
        l2_trwa = st.number_input("L2: Trwa ile (miesięcy)", value=3)
    with col3:
        st.markdown("**Lokata 3**")
        l3_kwota = st.number_input("L3: Ile Milionów", value=20.0)
        l3_start = st.number_input("L3: Start za (miesięcy)", value=7)
        l3_trwa = st.number_input("L3: Trwa ile (miesięcy)", value=3)

    if st.button("Generuj wynik końcowy na zaliczenie (Strip FRA)"):
        st.success("### Co napisać o Obligacjach? (Firma ucieka przed wzrostem stóp)")
        st.markdown("Ponieważ firma musi płacić odsetki od długu inwestorom, otwiera pozycję **DŁUGĄ (KUPNO FRA - bierze kursy wyższe ASK)**, pociętą na następujące części:")
        
        for i in range(liczba_okresow):
            początek = start_obl + (i * okres_obl)
            koniec = początek + okres_obl
            kontrakt = f"{początek}X{koniec}"
            st.markdown(f"- **Rata/Okres nr {i+1}:** Potrzebujemy kontraktu FRA **{kontrakt}** na nominał {kwota_obl} mln PLN. Bierzemy pozycję **KUPNO (Long)**.")
            st.latex(rf"\text{{Calkowity Koszt dla Okresu {i+1}}} = \text{{Cena FRA (ASK)}}_{{{kontrakt}}} + {marza_obl}\%")

        st.info("### Co napisać o Lokatach? (Firma ucieka przed spadkiem stóp)")
        st.markdown("Przy lokatach firma chce uchronić zyski, dlatego z każdą z lokat otwiera pozycję **KRÓTKĄ (SPRZEDAŻ FRA - bierze kursy niższe BID)**.")
        
        lokaty = [
            (l1_start, l1_trwa, l1_kwota, "Lokata 1 z zadania"),
            (l2_start, l2_trwa, l2_kwota, "Lokata 2 z zadania"),
            (l3_start, l3_trwa, l3_kwota, "Lokata 3 z zadania")
        ]
        
        for start, trwa, kwota, nazwa in lokaty:
            if kwota > 0:
                kontrakt = f"{start}X{start+trwa}"
                st.markdown(f"- **{nazwa}:** Potrzebny kontrakt o nazwie **{kontrakt}** na {kwota} mln PLN. Zaznacz pozycję: **SPRZEDAŻ (Short)**.")
                st.latex(rf"\text{{Efektywny Przychod ({nazwa})}} = \text{{Cena FRA (BID)}}_{{{kontrakt}}}")

# --------------------------------------------------------------------------------
# MODUŁ 9: BAZA WIEDZY I TEORII
# --------------------------------------------------------------------------------
elif opcja == "9. Wyszukiwarka Teorii (Baza Wiedzy)":
    st.header("📚 Wyszukiwarka Pojęć i Teorii (Baza Wiedzy)")
    st.info("💡 **Instrukcja:** Wpisz słowo kluczowe (np. 'aprecjacja') lub CAŁE pytanie z kolokwium. System na bazie algorytmu przeanalizuje wykłady i wskaże najważniejsze informacje, omijając nieważne słowa.")
    
    # Baza wiedzy została przepisana całkowicie na nowo własnymi słowami, aby system nie wstrzykiwał ukrytych znaczników
    baza_wiedzy = {
        "Aprecjacja a Deprecjacja": "Aprecjacja oznacza wzrost wartości krajowego pieniądza (za waluty obce płacimy mniej). Skutkuje to tańszym importem, ale nasz eksport staje się droższy dla zagranicy. Deprecjacja to spadek wartości naszej waluty (obce waluty drożeją). Import staje się droższy (rośnie inflacja), lecz eksport zyskuje na opłacalności.",
        "Dewaluacja a Rewaluacja": "Są to pojęcia zbliżone do aprecjacji i deprecjacji, jednak wynikają z oficjalnych decyzji władz monetarnych (banku centralnego) w systemach kursu stałego, a nie z rynkowej gry popytu i podaży.",
        "Waluta Kwotowana i Bazowa": "Dla pary walutowej takiej jak USD/PLN, pierwsza z nich (USD) to waluta bazowa (jej wartość wynosi zawsze 1), natomiast druga (PLN) to waluta kwotowana (określa cenę jednej jednostki bazowej). Kurs kupna (Bid) to cena zakupu waluty bazowej przez bank, a Ask to cena jej sprzedaży.",
        "Hedging (Zabezpieczenie)": "Jest to strategia ochrony przed ryzykiem kursowym polegająca na zajęciu pozycji przeciwstawnej do posiadanej ekspozycji. Wyróżniamy metody wewnętrzne (np. fakturowanie we własnej walucie) oraz zewnętrzne (użycie instrumentów takich jak kontrakty forward, futures czy opcje).",
        "Spekulacja a Arbitraż": "Spekulant podejmuje ryzyko, otwierając pozycję z nadzieją na zysk dzięki trafnym prognozom przyszłych kursów. Arbitrażysta z kolei poszukuje zysku bez ponoszenia ryzyka, dokonując jednoczesnego zakupu i sprzedaży na różnych rynkach, aby wykorzystać chwilowe różnice w cenach.",
        "Rynek Kasowy (Spot) vs Terminowy": "Rynek Spot (kasowy) to transakcje realizowane po bieżącym kursie z dostawą środków natychmiast lub maksymalnie w ciągu dwóch dni roboczych. Rynek terminowy to umowy ustalające cenę dzisiaj, ale z fizyczną dostawą waluty w z góry określonym dniu w przyszłości.",
        "Pozycja Walutowa Długa i Krótka": "Pozycja długa (Long) występuje, gdy posiadamy więcej aktywów i należności w walucie obcej niż zobowiązań (boimy się wtedy spadku jej kursu). Pozycja krótka (Short) oznacza przewagę zobowiązań nad należnościami w walucie obcej (zagrożeniem jest wtedy wzrost jej kursu).",
        "Teoria Parytetu Siły Nabywczej (PPP)": "Bazuje na Prawie Jednej Ceny – te same dobra powinny kosztować tyle samo w różnych krajach po przeliczeniu walut. W ujęciu absolutnym kurs zależy od poziomu cen, a w ujęciu względnym zmiany kursu wynikają z różnic w stopach inflacji pomiędzy państwami.",
        "Efekt Fishera i Międzynarodowy Efekt Fishera": "Zgodnie z efektem Fishera stopa nominalna to suma stopy realnej i oczekiwanej inflacji. Wersja międzynarodowa zakłada, że różnice w stopach procentowych między krajami determinują zmiany kursu – waluta kraju o wyższej stopie procentowej (i wyższej inflacji) będzie ulegać osłabieniu.",
        "Teoria Parytetu Stóp Procentowych (IRP)": "Teoria wiążąca rynki spot i forward. Wskazuje, że waluta kraju z wyższymi stopami procentowymi będzie notowana z dyskontem na rynku terminowym w stosunku do waluty kraju o niższych stopach procentowych.",
        "Teoria Oczekiwań": "Zakłada, że dzisiejszy kurs terminowy (forward) odzwierciedla rynkowe przewidywania i jest najlepszym oszacowaniem przyszłego kursu natychmiastowego (spot) w dniu wygaśnięcia kontraktu.",
        "Czynniki Wpływające na Kurs Walutowy": "Wzmocnienie waluty następuje na skutek wzrostu PKB, wyższych stóp procentowych czy dodatniego salda bilansu płatniczego. Osłabienie waluty wywołuje wysoka inflacja, rosnące bezrobocie oraz ujemny bilans płatniczy.",
        "Kontrakty Forward vs Futures": "Forward to elastyczne umowy pozagiełdowe dopasowane do klienta, ale obarczone ryzykiem niewypłacalności drugiej strony. Futures to standaryzowane kontrakty giełdowe, w których bezpieczeństwo zapewnia izba rozliczeniowa poprzez system depozytów zabezpieczających.",
        "Depozyty i Rozliczenia na Giełdzie Futures": "Izba rozliczeniowa wymaga wniesienia depozytu początkowego (przy otwarciu pozycji) oraz utrzymania depozytu podtrzymującego. Codziennie następuje wycena rynkowa (marking-to-market), która polega na dopisywaniu zysków lub potrącaniu strat z rachunku inwestora.",
        "Opcje Walutowe (Call, Put, Wartość)": "Dają kupującemu prawo (nie obowiązek) do zawarcia transakcji w zamian za zapłaconą premię. Wystawca pobiera premię, ale jego ryzyko straty jest teoretycznie nieograniczone. Opcja Call to prawo kupna, a Put – prawo sprzedaży. Wartość opcji to suma wartości wewnętrznej oraz wartości w czasie.",
        "Swap Walutowy (FX Swap)": "Obejmuje jednoczesne zawarcie transakcji spot (np. kupno waluty) i transakcji terminowej (odsprzedaż tej samej waluty w przyszłości). Pozwala na krótkoterminowe pozyskanie waluty bez wystawiania się na ryzyko kursowe.",
        "Swap Stopy Procentowej (IRS)": "Transakcja bez fizycznej wymiany kapitału docelowego. Strony wymieniają się wyłącznie płatnościami odsetkowymi w tej samej walucie. Często wykorzystywana do zamiany oprocentowania zmiennego na stałe.",
        "Swap Walutowo-Procentowy (CIRS)": "Składa się z trzech kroków: początkowej wymiany nominałów w różnych walutach, cyklicznej wymiany płatności odsetkowych w tych walutach oraz zwrotu nominałów na koniec umowy. Pomaga firmom taniej pozyskiwać kapitał zagranicą.",
        "Międzynarodowy Fundusz Walutowy (MFW / IMF)": "Organizacja powstała w 1944 r. w Bretton Woods. Jej zadaniem jest nadzór nad globalnym systemem finansowym, promowanie współpracy i udzielanie pomocy kredytowej krajom borykającym się z kryzysami bilansu płatniczego. Jednostką rozliczeniową MFW jest SDR.",
        "Grupa Banku Światowego (WBG)": "W jej skład wchodzi m.in. Międzynarodowy Bank Odbudowy i Rozwoju (IBRD) oraz Międzynarodowe Stowarzyszenie Rozwoju (IDA), które udziela preferencyjnych, nieoprocentowanych kredytów dla najbiedniejszych krajów na świecie.",
        "Instytucje Banku Światowego dla Biznesu": "IFC wspiera prywatne przedsiębiorstwa udzielając im pożyczek bez gwarancji rządowych. MIGA oferuje ubezpieczenia dla inwestorów przed ryzykiem politycznym (np. wojną czy nacjonalizacją). ICSID pełni funkcję sądu arbitrażowego w sporach inwestycyjnych.",
        "System Izby Walutowej (Currency Board)": "To reżim bardzo sztywnego kursu walutowego, w którym państwo rezygnuje z niezależnej polityki pieniężnej na rzecz powiązania własnej waluty z obcą (np. z dolarem). Cała baza monetarna musi mieć pokrycie w rezerwach dewizowych.",
        "Waluta Międzynarodowa i Jej Funkcje": "Wybór waluty w transakcjach globalnych zależy od potęgi gospodarki i zaufania do emitenta. Pełni ona funkcje: waluty rezerwowej, waluty fakturowania (w rozliczeniach handlowych), waluty interwencyjnej (dla banków centralnych) i waluty transakcyjnej na Forexie."
    }

    query = st.text_input("Wpisz pytanie lub słowo klucz (np. 'czym różni się forward od futures', 'efekt fishera', 'mfw')", "")

    if query:
        def normalize_text(text):
            replacements = {'ą':'a', 'ć':'c', 'ę':'e', 'ł':'l', 'ń':'n', 'ó':'o', 'ś':'s', 'ź':'z', 'ż':'z'}
            text = text.lower()
            for k, v in replacements.items():
                text = text.replace(k, v)
            return text

        query_norm = normalize_text(query)
        words = re.findall(r'\w+', query_norm)
        
        # Odrzucamy słowa, które nic nie wnoszą do kontekstu wyszukiwania
        stop_words = {"co", "to", "jest", "jak", "dlaczego", "kiedy", "gdzie", "wymien", "podaj", "czym", "sie", "i", "oraz", "na", "w", "z", "o", "a", "od", "do"}
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        results = []
        for title, desc in baza_wiedzy.items():
            score = 0
            t_norm = normalize_text(title)
            d_norm = normalize_text(desc)
            
            # Punktacja za dokładne trafienia całej frazy (najcenniejsze)
            if query_norm in t_norm:
                score += 100
            if query_norm in d_norm:
                score += 50
                
            # Punktacja za poszczególne rozbite słowa kluczowe
            for kw in keywords:
                if kw in t_norm:
                    score += 10
                if kw in d_norm:
                    score += 3
                    
            if score > 0:
                results.append((score, title, desc))

        results.sort(key=lambda x: x[0], reverse=True)

        if results:
            st.success(f"Znaleziono {len(results)} pasujących zagadnień na podstawie Twojego pytania:")
            for score, title, desc in results[:5]: # ograniczamy do top 5 wyników
                st.markdown(f"### 📘 {title}")
                st.write(desc)
                st.markdown("---")
        else:
            st.warning("Nie znaleziono pasującego zagadnienia w bazie. Spróbuj użyć innego, pojedynczego słowa kluczowego (np. wpisz samo słowo 'opcje' zamiast całego zdania).")
    else:
        st.info("Baza danych załadowana z sukcesem z materiałów wykładowych. Czekam na Twoje zapytanie...")
        
        with st.expander("Przeglądaj wszystkie definicje (Alfabetycznie)"):
            for title, desc in sorted(baza_wiedzy.items()):
                st.markdown(f"**{title}** - {desc}")
