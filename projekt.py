import openai
import os
import re
import time

# Twój klucz API OpenAI
API_KEY = "Twój_klucz_API"  # Wstaw swój klucz API
openai.api_key = API_KEY

def generate_html_with_numbered_images(article_content, image_count):
    prompt = (
        f"Przekaż poniższy tekst w strukturze HTML bez sekcji <html>, <head> lub <body>. "
        f"Dodaj odpowiednie znaczniki nagłówka i akapitu. "
        f"Wstaw dokładnie {image_count} obrazków, rozmieszczając je równomiernie w miejscach, które dobrze pasują do kontekstu. "
        "Każdy obraz ma mieć unikalny numer w nazwie pliku w atrybucie src, zaczynając od 'image_placeholder1.jpg', 'image_placeholder2.jpg' i tak dalej, aż do podanej liczby obrazów. "
        "Dodaj również alt opisujący treść obrazka oraz podpis pod obrazkiem. Oto treść artykułu:\n\n" + article_content
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Jesteś asystentem wspomagającym formatowanie artykułów do HTML."},
            {"role": "user", "content": prompt}
        ]
    )

    assistant_response = response['choices'][0]['message']['content']
    
    return assistant_response.strip()

def remove_image(html_content, image_number):
    pattern = rf'<img src="image_placeholder{image_number}\.jpg"[^>]*>'
    updated_html, count = re.subn(pattern, '', html_content)
    
    if count > 0:
        print(f"Obrazek image_placeholder{image_number}.jpg został usunięty.")
    else:
        print(f"Obrazek image_placeholder{image_number}.jpg nie istnieje.")
    
    return updated_html

def swap_images(html_content, img1, img2):
    pattern1 = rf'(src="image_placeholder{img1}\.jpg")'
    pattern2 = rf'(src="image_placeholder{img2}\.jpg")'
    
    if re.search(pattern1, html_content) and re.search(pattern2, html_content):
        html_content = re.sub(pattern1, "TEMP_IMG", html_content)
        html_content = re.sub(pattern2, f'src="image_placeholder{img1}.jpg"', html_content)
        html_content = re.sub("TEMP_IMG", f'src="image_placeholder{img2}.jpg"', html_content)
        print(f"\nObrazki image_placeholder{img1}.jpg i image_placeholder{img2}.jpg zostały zamienione miejscami.")
    else:
        print("\nNie można zamienić obrazków - jeden z numerów nie istnieje.")
    
    return html_content

def regenerate_image(html_content, image_number, article_content, image_count):
    print("Wybierz sposób generowania nowego opisu i podpisu:")
    print("1. Automatyczne wygenerowanie opisu przez ChatGPT na podstawie istniejącego tekstu")
    print("2. Podanie własnego opisu do obrazka")
    print("3. Generowanie nowego opisu przez ChatGPT na podstawie własnych wskazówek")

    choice = input("Wpisz '1', '2' lub '3' i naciśnij Enter: ").strip()
    
    alt_pattern = rf'<img src="image_placeholder{image_number}\.jpg" alt="([^"]*)"'
    caption_pattern = rf'<p><em>Rys. {image_number}: (.*?)</em></p>'
    
    current_alt = re.search(alt_pattern, html_content)
    current_caption = re.search(caption_pattern, html_content)

    if choice == '1':
        # Wybieramy fragment artykułu, który najlepiej pasuje do obrazu (np. pierwsze 500 znaków)
        base_text = article_content[:500]  # Ograniczamy długość do 500 znaków
        prompt = f"Na podstawie poniższego tekstu wygeneruj opis (alt) i podpis do obrazka:\n\n'{base_text}'\n\nOpis obrazu:"

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś asystentem wspomagającym formatowanie artykułów do HTML."},
                {"role": "user", "content": prompt}
            ]
        )
        
        new_description = response['choices'][0]['message']['content'].strip()
        # Sprawdzamy, czy opis zawiera oddzielne linie dla alt i podpisu
        if "\n" in new_description:
            new_alt, new_caption = new_description.split("\n", 1)
        else:
            new_alt, new_caption = new_description, new_description

    elif choice == '2':
        new_alt = input("Podaj nowy opis (alt) dla obrazka: ")
        new_caption = input("Podaj nowy podpis dla obrazka (np. 'Sieci neuronowe i uczenie maszynowe'): ")

    elif choice == '3':
        user_suggestion = input("Podaj opis lub wskazówki do wygenerowania bardziej szczegółowego opisu i podpisu: ")
        prompt = f"Stwórz szczegółowy opis (alt) oraz podpis na podstawie następujących wskazówek: '{user_suggestion}'"
        
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś asystentem wspomagającym formatowanie artykułów do HTML."},
                {"role": "user", "content": prompt}
            ]
        )
        
        new_description = response['choices'][0]['message']['content'].strip()
        if "\n" in new_description:
            new_alt, new_caption = new_description.split("\n", 1)
        else:
            new_alt, new_caption = new_description, new_description
    
    else:
        print("Nieznana opcja. Wybierz '1', '2', lub '3'.")
        return html_content  

    # Zastępujemy stare opisy nowymi
    if current_alt:
        html_content = re.sub(alt_pattern, f'<img src="image_placeholder{image_number}.jpg" alt="{new_alt}"', html_content)
    if current_caption:
        html_content = re.sub(caption_pattern, f'<p><em>Rys. {image_number}: {new_caption}</em></p>', html_content)
    else:
        image_tag_pattern = rf'<img src="image_placeholder{image_number}\.jpg"[^>]*>'
        html_content = re.sub(image_tag_pattern, f'\\g<0>\n<p><em>Rys. {image_number}: {new_caption}</em></p>', html_content)

    print(f"Obrazek {image_number} został zaktualizowany z nowym opisem i podpisem.")
    
    return html_content

def show_menu():
    print("\n=========================================")
    print("       Opcje do wyboru:")
    print("=========================================")
    print("1. Wygeneruj nowe miejsca dla obrazków (Wpisz 'jeszcze raz')")
    print("2. Usuń obrazek (Wpisz 'usuń <numer>', np. 'usuń 3')")
    print("3. Zamień miejscami obrazki (Wpisz 'zamień <numer1> <numer2>', np. 'zamień 1 3')")
    print("4. Wygeneruj obrazek na nowo (Wpisz 'wygeneruj <numer>', np. 'wygeneruj 2')")
    print("5. Zapisz i zakończ (Wpisz 'zapisz')")
    print("=========================================")

def main():
    if not os.path.isfile("projekt.txt"):
        print("Błąd: Plik 'projekt.txt' nie istnieje.")
        return
    with open("projekt.txt", "r", encoding="utf-8") as file:
        article_content = file.read()

    while True:
        try:
            image_count = int(input("Podaj liczbę obrazów do wygenerowania w artykule: "))
            if image_count < 0:
                print("Liczba obrazów nie może być ujemna.")
                continue
        except ValueError:
            print("Proszę podać poprawną liczbę całkowitą.")
            continue

        generated_html = generate_html_with_numbered_images(article_content, image_count)
        print("Wygenerowany artykuł z obrazkami:")
        print(generated_html)

        while True:
            show_menu()
            user_input = input("Wybierz opcję: ").strip().lower()

            if user_input == "zapisz":
                with open("artykul.html", "w", encoding="utf-8") as file:
                    file.write(generated_html)
                print("Plik zapisany jako 'artykul.html'.")
                return

            elif user_input == "jeszcze raz":
                break

            elif user_input.startswith("usuń "):
                try:
                    image_number = int(user_input.split()[1])
                    generated_html = remove_image(generated_html, image_number)
                except (ValueError, IndexError):
                    print("Niepoprawny numer obrazka do usunięcia.")

            elif user_input.startswith("zamień "):
                try:
                    img1, img2 = map(int, user_input.split()[1:3])
                    generated_html = swap_images(generated_html, img1, img2)
                except (ValueError, IndexError):
                    print("Podaj dwa poprawne numery obrazków do zamiany.")

            elif user_input.startswith("wygeneruj "):
                try:
                    image_number = int(user_input.split()[1])
                    generated_html = regenerate_image(generated_html, image_number, article_content, image_count)
                except (ValueError, IndexError):
                    print("Niepoprawny numer obrazka do ponownego wygenerowania.")

            else:
                print("Nieznana komenda. Użyj 'jeszcze raz', 'usuń <numer>', 'zamień <numer1> <numer2>', 'wygeneruj <numer>' lub 'zapisz'.")
            
            time.sleep(1)

if __name__ == "__main__":
    main()
