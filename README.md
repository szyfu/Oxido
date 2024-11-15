# Oxido
Opis działania aplikacji:
Aplikacja jest narzędziem wspierającym tworzenie artykułów w formacie HTML, w którym użytkownik może generować obrazy, modyfikować je (usuwać, zamieniać miejscami, regenerować opisy i podpisy) oraz zapisać wynikowy artykuł do pliku HTML. Całość bazuje na API OpenAI, które jest wykorzystywane do generowania opisów i podpisów do obrazków na podstawie artykułu.

Główne funkcje:

Generowanie HTML z obrazkami – Aplikacja przyjmuje artykuł w formie tekstowej i generuje odpowiedni kod HTML. Wstawiane są obrazki (w ilości określonej przez użytkownika), a każdy obrazek ma przypisany unikalny numer oraz automatycznie generowany opis (alt) i podpis.
Usuwanie obrazków – Użytkownik może usunąć wskazany obrazek z wygenerowanego HTML, podając jego numer.
Zamiana miejscami obrazków – Aplikacja umożliwia zamianę miejscami dwóch obrazków, jeśli oba istnieją w artykule.
Regenerowanie opisów i podpisów – Użytkownik może zaktualizować opis (alt) i podpis obrazka na kilka sposobów:
Automatycznie na podstawie kontekstu artykułu.
Własnoręcznie wprowadzając tekst.
Generując szczegółowy opis i podpis na podstawie własnych wskazówek.
Zapis i zakończenie – Po zakończeniu edycji użytkownik może zapisać wygenerowany artykuł HTML do pliku.
Instrukcja uruchomienia aplikacji:
1. Zainstalowanie wymaganych bibliotek:

Aby uruchomić aplikację, należy mieć zainstalowaną bibliotekę openai, której używamy do generowania treści za pomocą modelu GPT-4.

Uruchom poniższą komendę, aby zainstalować wymagane biblioteki:

pip install openai
2. Wstawienie własnego klucza API:

Zarejestruj się na platformie OpenAI i uzyskaj swój klucz API.
Zamień wartość zmiennej API_KEY w kodzie na swój klucz API. Należy to zrobić w miejscu, gdzie klucz jest przypisany:
API_KEY = "Twój_klucz_API"
openai.api_key = API_KEY
3. Przygotowanie pliku z artykułem:

Przygotuj plik tekstowy o nazwie projekt.txt, który będzie zawierał treść artykułu. Aplikacja wczytuje ten plik i na podstawie jego zawartości generuje HTML.
Upewnij się, że plik projekt.txt jest w tym samym folderze, co skrypt Pythona.
4. Uruchomienie aplikacji:

Aby uruchomić aplikację, wystarczy wykonać poniższą komendę w terminalu, w folderze z plikiem skryptu:
python nazwa_skryptu.py
Zastąp nazwa_skryptu.py nazwą pliku, w którym zapisano kod.

5. Interakcja z aplikacją:

Po uruchomieniu aplikacji, użytkownik zostanie poproszony o:

Podanie liczby obrazków – Określa, ile obrazków ma być dodanych do wygenerowanego artykułu.
Dalszą interakcję za pomocą menu – W menu użytkownik ma następujące opcje:
Wygenerowanie nowych miejsc dla obrazków – Generowanie nowego artykułu HTML z obrazkami.
Usunięcie obrazka – Usunięcie wskazanego obrazka na podstawie numeru.
Zamiana miejscami obrazków – Zamiana dwóch obrazków na podstawie numerów.
Wygenerowanie nowego opisu i podpisu do obrazka – Użytkownik może wybrać, jak chce wygenerować nowe opisy (automatycznie, ręcznie lub na podstawie wskazówek).
Zapisanie artykułu i zakończenie – Zapisanie wygenerowanego HTML do pliku i zakończenie pracy z aplikacją.
6. Przykład działania:

Uruchom aplikację.
Podaj liczbę obrazków, które mają zostać dodane do artykułu.
Wygenerowany artykuł HTML z obrazkami zostanie wyświetlony.
Skorzystaj z menu, aby wykonać operacje na obrazkach (usuń, zamień, regeneruj opisy).
Po zakończeniu możesz zapisać artykuł w pliku generated_article.html.
Przykład działania aplikacji:
Krok 1: Wprowadź liczbę obrazków:

Podaj liczbę obrazów do wygenerowania w artykule: 3
Krok 2: Wybór opcji z menu:

=========================================
       Opcje do wyboru:
=========================================
1. Wygeneruj nowe miejsca dla obrazków (Wpisz 'jeszcze raz')
2. Usuń obrazek (Wpisz 'usuń <numer>', np. 'usuń 3')
3. Zamień miejscami obrazki (Wpisz 'zamień <numer1> <numer2>', np. 'zamień 1 3')
4. Wygeneruj obrazek na nowo (Wpisz 'wygeneruj <numer>', np. 'wygeneruj 2')
5. Zapisz i zakończ (Wpisz 'zapisz')
=========================================
Krok 3: Wybór opcji – Przykład "wygeneruj 2":

Wybierz sposób generowania nowego opisu i podpisu:
1. Automatyczne wygenerowanie opisu przez ChatGPT na podstawie istniejącego tekstu
2. Podanie własnego opisu do obrazka
3. Generowanie nowego opisu przez ChatGPT na podstawie własnych wskazówek
Wpisz '1', '2' lub '3' i naciśnij Enter: 1
Krok 4: Zapisz plik HTML:

Plik zapisany jako 'generated_article.html'.
Aplikacja zakończy działanie po zapisaniu pliku.
