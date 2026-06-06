"""
🎮 PRONUNCIATION CHALLENGE - English Learning Game
Un juego de consola para practicar la pronunciación en inglés
"""

import speech_recognition as sr
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import os
import sys
from googletrans import Translator
import time
import random

# Colores ANSI para la terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

# Base de palabras en español con traducciones en inglés
WORDS_DATABASE = {
    "fácil": {
        "english": "easy",
        "difficulty": 1
    },
    "gato": {
        "english": "cat",
        "difficulty": 1
    },
    "perro": {
        "english": "dog",
        "difficulty": 1
    },
    "casa": {
        "english": "house",
        "difficulty": 1
    },
    "agua": {
        "english": "water",
        "difficulty": 1
    },
    "libro": {
        "english": "book",
        "difficulty": 1
    },
    "árbol": {
        "english": "tree",
        "difficulty": 1
    },
    "computadora": {
        "english": "computer",
        "difficulty": 2
    },
    "traducción": {
        "english": "translation",
        "difficulty": 2
    },
    "biblioteca": {
        "english": "library",
        "difficulty": 2
    },
    "vocabulario": {
        "english": "vocabulary",
        "difficulty": 2
    },
    "pronunciación": {
        "english": "pronunciation",
        "difficulty": 3
    },
    "comunicación": {
        "english": "communication",
        "difficulty": 3
    },
    "inteligencia": {
        "english": "intelligence",
        "difficulty": 3
    },
    "desarrollo": {
        "english": "development",
        "difficulty": 3
    }
}

class PronunciationGame:
    def __init__(self):
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.difficulty_level = 1
        self.total_rounds = 5
        self.current_round = 0
        self.recognizer = sr.Recognizer()
        self.translator = Translator()
        
    def clear_screen(self):
        """Limpia la pantalla"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Imprime el encabezado del juego"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║        🎮 PRONUNCIATION CHALLENGE - English Game 🎮        ║")
        print("║          Practica tu pronunciación en inglés             ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print(f"{Colors.END}")
    
    def show_menu(self):
        """Muestra el menú principal"""
        self.clear_screen()
        self.print_header()
        print(f"\n{Colors.YELLOW}📋 MENÚ PRINCIPAL{Colors.END}\n")
        print("1️⃣  Jugar - Fácil (5 palabras con voz)")
        print("2️⃣  Jugar - Normal (5 palabras con voz)")
        print("3️⃣  Jugar - Difícil (5 palabras con voz)")
        print("4️⃣  ⚡ MINIJUEGO - Flash Words (Velocidad)")
        print("5️⃣  🐝 MINIJUEGO - Spelling Bee (Deletreo)")
        print("6️⃣  🧠 MINIJUEGO - Memory Match (Memoria)")
        print("7️⃣  📊 Estadísticas")
        print("8️⃣  Salir")
        print("\n" + "─" * 60)
        
    def select_difficulty(self, difficulty):
        """Selecciona el nivel de dificultad"""
        difficulty_map = {
            1: ("Fácil 😊", 1),
            2: ("Normal 🤔", 2),
            3: ("Difícil 🔥", 3)
        }
        
        name, level = difficulty_map.get(difficulty, ("Fácil", 1))
        self.difficulty_level = level
        print(f"\n{Colors.BLUE}✅ Dificultad seleccionada: {name}{Colors.END}")
        time.sleep(1.5)
        
    def get_words_by_difficulty(self):
        """Obtiene palabras según el nivel de dificultad"""
        words = {}
        for spanish, data in WORDS_DATABASE.items():
            if data["difficulty"] <= self.difficulty_level:
                words[spanish] = data["english"]
        return words
    
    def record_audio(self, duration=5, sample_rate=16000):
        """Graba audio del usuario"""
        print(f"\n{Colors.YELLOW}🎤 Grabando en 3 segundos... Prepárate!{Colors.END}")
        for i in range(3, 0, -1):
            print(f"   ⏳ {i}...", end="\r")
            time.sleep(1)
        
        print(f"   {Colors.GREEN}🔴 GRABANDO...{Colors.END}      ", end="\r")
        
        try:
            audio = sd.rec(int(duration * sample_rate), 
                         samplerate=sample_rate, 
                         channels=1, 
                         dtype=np.int16)
            sd.wait()
            
            # Guardar el audio temporalmente
            wavfile.write("temp_audio.wav", sample_rate, audio)
            print(f"   {Colors.GREEN}✅ Grabación completada!{Colors.END}     ")
            return True
        except Exception as e:
            print(f"\n{Colors.RED}❌ Error al grabar: {str(e)}{Colors.END}")
            return False
    
    def recognize_speech(self):
        """Reconoce el habla del usuario"""
        try:
            print(f"{Colors.YELLOW}🧠 Procesando el audio...{Colors.END}")
            
            with sr.AudioFile("temp_audio.wav") as source:
                audio_data = self.recognizer.record(source)
            
            recognized_text = self.recognizer.recognize_google(audio_data, language='en-US')
            print(f"{Colors.GREEN}✅ Audio reconocido: '{recognized_text}'{Colors.END}")
            return recognized_text.lower()
        
        except sr.UnknownValueError:
            print(f"{Colors.RED}❌ No se pudo entender el audio. Intenta de nuevo.{Colors.END}")
            return None
        except sr.RequestError:
            print(f"{Colors.RED}❌ Error de conexión con el servicio de reconocimiento.{Colors.END}")
            return None
        except Exception as e:
            print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")
            return None
        finally:
            # Limpiar archivo temporal
            if os.path.exists("temp_audio.wav"):
                try:
                    os.remove("temp_audio.wav")
                except:
                    pass
    
    def compare_words(self, recognized, expected):
        """Compara la palabra reconocida con la esperada"""
        # Permite pequeñas variaciones (plural, conjugaciones simples)
        recognized_clean = recognized.strip().lower()
        expected_clean = expected.strip().lower()
        
        # Comparación exacta
        if recognized_clean == expected_clean:
            return True
        
        # Comparación flexible (contiene la palabra)
        if expected_clean in recognized_clean or recognized_clean in expected_clean:
            return True
        
        # Permite plurales simples
        if recognized_clean.rstrip('s') == expected_clean or \
           recognized_clean == expected_clean.rstrip('s'):
            return True
        
        return False
    
    def play_round(self, word_spanish, word_english):
        """Juega una ronda del juego"""
        self.current_round += 1
        print(f"\n{Colors.CYAN}{'='*60}{Colors.END}")
        print(f"{Colors.BOLD}📚 RONDA {self.current_round} / {self.total_rounds}{Colors.END}")
        print(f"{Colors.CYAN}{'='*60}{Colors.END}")
        
        print(f"\n{Colors.YELLOW}La palabra en español es:{Colors.END}")
        print(f"{Colors.BOLD}{Colors.BLUE}👉 {word_spanish.upper()} 👈{Colors.END}\n")
        
        print(f"{Colors.YELLOW}Tu tarea:{Colors.END}")
        print(f"🎤 Pronuncia esta palabra en INGLÉS cuando veas el mensaje de grabación\n")
        
        input(f"{Colors.YELLOW}Presiona ENTER cuando estés listo...{Colors.END}")
        
        # Grabar audio
        if not self.record_audio(duration=4):
            print(f"{Colors.RED}❌ Intenta de nuevo en la siguiente ronda.{Colors.END}")
            self.incorrect_answers += 1
            return
        
        # Reconocer el habla
        recognized_text = self.recognize_speech()
        if recognized_text is None:
            print(f"{Colors.RED}❌ No se pudo reconocer tu pronunciación.{Colors.END}")
            self.incorrect_answers += 1
            return
        
        # Comparar
        print(f"\n{Colors.YELLOW}La palabra esperada era: {word_english}{Colors.END}")
        
        if self.compare_words(recognized_text, word_english):
            points = 10 * self.difficulty_level
            self.score += points
            self.correct_answers += 1
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ¡CORRECTO! +{points} puntos 🎉{Colors.END}")
        else:
            self.incorrect_answers += 1
            print(f"\n{Colors.RED}{Colors.BOLD}❌ Incorrecto ❌{Colors.END}")
            print(f"{Colors.YELLOW}Dijiste: '{recognized_text}'{Colors.END}")
            print(f"{Colors.YELLOW}Esperado: '{word_english}'{Colors.END}")
        
        print(f"\n{Colors.BLUE}Puntuación actual: {self.score} puntos{Colors.END}")
        time.sleep(2)
    
    def show_stats(self):
        """Muestra las estadísticas del juego"""
        self.clear_screen()
        self.print_header()
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}📊 ESTADÍSTICAS{Colors.END}\n")
        print(f"Total de puntos: {Colors.GREEN}{self.score}{Colors.END}")
        print(f"Respuestas correctas: {Colors.GREEN}{self.correct_answers}✅{Colors.END}")
        print(f"Respuestas incorrectas: {Colors.RED}{self.incorrect_answers}❌{Colors.END}")
        
        if self.correct_answers + self.incorrect_answers > 0:
            accuracy = (self.correct_answers / (self.correct_answers + self.incorrect_answers)) * 100
            print(f"Precisión: {Colors.YELLOW}{accuracy:.1f}%{Colors.END}")
        
        print(f"\n{'─'*60}")
        input(f"{Colors.YELLOW}Presiona ENTER para volver al menú...{Colors.END}")
    
    def play_game(self, difficulty):
        """Inicia una partida completa"""
        self.clear_screen()
        self.print_header()
        
        # Seleccionar dificultad
        self.select_difficulty(difficulty)
        self.score = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.current_round = 0
        
        # Obtener palabras según dificultad
        words = self.get_words_by_difficulty()
        
        if not words:
            print(f"{Colors.RED}❌ No hay palabras disponibles para esta dificultad.{Colors.END}")
            return
        
        # Convertir a lista
        words_list = list(words.items())
        
        # Limitar a 5 palabras aleatorias
        import random
        selected_words = random.sample(words_list, min(self.total_rounds, len(words_list)))
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}🎮 ¡Comienza el juego!{Colors.END}")
        print(f"{Colors.YELLOW}Tendrás {self.total_rounds} rondas para practicar tu pronunciación.{Colors.END}\n")
        
        input(f"{Colors.YELLOW}Presiona ENTER para empezar...{Colors.END}")
        
        # Jugar rondas
        for spanish, english in selected_words:
            self.play_round(spanish, english)
        
        # Mostrar resultado final
        self.show_final_results()
    
    def show_final_results(self):
        """Muestra los resultados finales"""
        self.clear_screen()
        self.print_header()
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}🏁 ¡JUEGO TERMINADO! 🏁{Colors.END}\n")
        
        print(f"{'━'*60}")
        print(f"📈 RESULTADOS FINALES")
        print(f"{'━'*60}\n")
        
        print(f"Total de rondas: {self.total_rounds}")
        print(f"Respuestas correctas: {Colors.GREEN}{self.correct_answers}✅{Colors.END}")
        print(f"Respuestas incorrectas: {Colors.RED}{self.incorrect_answers}❌{Colors.END}")
        
        if self.correct_answers + self.incorrect_answers > 0:
            accuracy = (self.correct_answers / (self.correct_answers + self.incorrect_answers)) * 100
            print(f"Precisión: {Colors.YELLOW}{accuracy:.1f}%{Colors.END}")
        
        print(f"\n{Colors.BOLD}Puntuación total: {Colors.GREEN}{self.score} PUNTOS{Colors.END}\n")
        
        # Mensaje de motivación
        if self.correct_answers == self.total_rounds:
            print(f"{Colors.GREEN}🌟 ¡PERFECTO! ¡Eres un campeón de la pronunciación! 🌟{Colors.END}")
        elif accuracy >= 80:
            print(f"{Colors.GREEN}🎯 ¡Excelente trabajo! Sigue practicando. 🎯{Colors.END}")
        elif accuracy >= 60:
            print(f"{Colors.YELLOW}💪 Buen esfuerzo. ¡Sigue mejorando! 💪{Colors.END}")
        else:
            print(f"{Colors.BLUE}📚 Sigue practicando, ¡lo lograrás! 📚{Colors.END}")
        
        print(f"\n{'─'*60}")
        input(f"{Colors.YELLOW}Presiona ENTER para volver al menú...{Colors.END}")
    
    def play_flash_words_minigame(self):
        """Minijuego de palabras relámpago - traduce palabras rápidamente"""
        self.clear_screen()
        self.print_header()
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}⚡ MINIJUEGO: FLASH WORDS ⚡{Colors.END}")
        print(f"{Colors.YELLOW}Palabras Relámpago - ¡Traduce lo más rápido que puedas!{Colors.END}\n")
        
        print(f"{Colors.BLUE}📋 REGLAS:{Colors.END}")
        print("1. Se te mostrará una palabra en español")
        print("2. ¡Tienes solo 10 SEGUNDOS para escribir la traducción en inglés!")
        print("3. ¡Cuanto más rápido respondas, más puntos ganas!")
        print("4. 15 palabras en total")
        print(f"\nPuntuación: 100 puntos si aciertas en menos de 5 segundos")
        print(f"            50 puntos si aciertas entre 5-10 segundos")
        print(f"            0 puntos si fallas o se acaba el tiempo\n")
        
        input(f"{Colors.YELLOW}Presiona ENTER para comenzar...{Colors.END}")
        
        flash_score = 0
        flash_correct = 0
        flash_rounds = 15
        all_words = list(WORDS_DATABASE.items())
        selected_words = random.sample(all_words, min(flash_rounds, len(all_words)))
        
        for idx, (spanish, data) in enumerate(selected_words, 1):
            english = data["english"]
            
            self.clear_screen()
            print(f"{Colors.CYAN}{Colors.BOLD}⚡ FLASH WORDS ⚡{Colors.END}")
            print(f"Ronda {idx}/{flash_rounds}\n")
            
            print(f"{Colors.YELLOW}La palabra es:{Colors.END}")
            print(f"{Colors.BOLD}{Colors.BLUE}{spanish.upper()}{Colors.END}\n")
            
            start_time = time.time()
            user_answer = input(f"{Colors.YELLOW}✍️ Tu respuesta: {Colors.END}").strip().lower()
            elapsed_time = time.time() - start_time
            
            # Verificar respuesta
            if user_answer == english or user_answer in english or english in user_answer:
                flash_correct += 1
                
                if elapsed_time < 5:
                    points = 100
                    print(f"\n{Colors.GREEN}🚀 ¡INCREÍBLE! +100 puntos (respondiste en {elapsed_time:.1f}s){Colors.END}")
                elif elapsed_time < 10:
                    points = 50
                    print(f"\n{Colors.GREEN}✅ ¡CORRECTO! +50 puntos (respondiste en {elapsed_time:.1f}s){Colors.END}")
                else:
                    points = 0
                    print(f"\n{Colors.YELLOW}⏰ Respondiste en {elapsed_time:.1f}s (fuera de tiempo, pero acertaste){Colors.END}")
                
                flash_score += points
            else:
                print(f"\n{Colors.RED}❌ ¡INCORRECTO!{Colors.END}")
                print(f"{Colors.YELLOW}La respuesta era: {english}{Colors.END}")
                print(f"{Colors.RED}Dijiste: {user_answer}{Colors.END}")
            
            print(f"{Colors.BLUE}Puntos este minijuego: {flash_score}{Colors.END}")
            time.sleep(1.5)
        
        # Resultado final del minijuego
        self.clear_screen()
        self.print_header()
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}🏁 ¡MINIJUEGO TERMINADO! 🏁{Colors.END}\n")
        print(f"{'━'*60}")
        print(f"⚡ RESULTADOS - FLASH WORDS ⚡")
        print(f"{'━'*60}\n")
        
        print(f"Palabras correctas: {Colors.GREEN}{flash_correct}/{flash_rounds}✅{Colors.END}")
        print(f"Puntuación del minijuego: {Colors.BOLD}{Colors.GREEN}{flash_score} PUNTOS{Colors.END}\n")
        
        accuracy = (flash_correct / flash_rounds) * 100
        
        if accuracy == 100:
            print(f"{Colors.GREEN}🌟 ¡PERFECTA RACHA! ¡Eres una máquina! 🌟{Colors.END}")
        elif accuracy >= 80:
            print(f"{Colors.GREEN}🚀 ¡EXCELENTE! Eres muy rápido. 🚀{Colors.END}")
        elif accuracy >= 60:
            print(f"{Colors.YELLOW}💪 ¡Buen trabajo! Sigue mejorando tu velocidad. 💪{Colors.END}")
        else:
            print(f"{Colors.BLUE}🎯 Practica más para mejorar tu velocidad. 🎯{Colors.END}")
        
        # Agregar puntos al total
        self.score += flash_score
        print(f"\n{Colors.GREEN}Los {flash_score} puntos se han añadido a tu puntuación total!{Colors.END}")
        print(f"{Colors.BLUE}Puntuación acumulada: {self.score}{Colors.END}\n")
        
        print(f"{'─'*60}")
        input(f"{Colors.YELLOW}Presiona ENTER para volver al menú...{Colors.END}")
    
    def play_spelling_bee_minigame(self):
        """Minijuego Spelling Bee - Deletrear palabras en inglés"""
        self.clear_screen()
        self.print_header()
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}🐝 MINIJUEGO: SPELLING BEE 🐝{Colors.END}")
        print(f"{Colors.YELLOW}¡Deletrea palabras en inglés correctamente!{Colors.END}\n")
        
        print(f"{Colors.BLUE}📋 REGLAS:{Colors.END}")
        print("1. Se te mostrará la pronunciación de una palabra en inglés")
        print("2. Debes escribir la palabra deletreada correctamente")
        print("3. 10 palabras en total")
        print(f"\nPuntuación: 20 puntos por palabra correcta\n")
        
        input(f"{Colors.YELLOW}Presiona ENTER para comenzar...{Colors.END}")
        
        spelling_score = 0
        spelling_correct = 0
        spelling_rounds = 10
        all_words = list(WORDS_DATABASE.items())
        selected_words = random.sample(all_words, min(spelling_rounds, len(all_words)))
        
        for idx, (spanish, data) in enumerate(selected_words, 1):
            english = data["english"]
            
            self.clear_screen()
            print(f"{Colors.CYAN}{Colors.BOLD}🐝 SPELLING BEE 🐝{Colors.END}")
            print(f"Ronda {idx}/{spelling_rounds}\n")
            
            print(f"{Colors.YELLOW}La palabra en español es: {spanish}{Colors.END}")
            print(f"{Colors.BLUE}En inglés se pronuncia como: {english}{Colors.END}\n")
            print(f"{Colors.YELLOW}¿Cómo se deletrea en inglés?{Colors.END}\n")
            
            user_answer = input(f"{Colors.YELLOW}✍️ Tu respuesta: {Colors.END}").strip().lower()
            
            # Verificar respuesta
            if user_answer == english:
                spelling_correct += 1
                spelling_score += 20
                print(f"\n{Colors.GREEN}✅ ¡CORRECTO! +20 puntos{Colors.END}")
            else:
                print(f"\n{Colors.RED}❌ ¡INCORRECTO!{Colors.END}")
                print(f"{Colors.YELLOW}La respuesta correcta era: {english}{Colors.END}")
                print(f"{Colors.RED}Dijiste: {user_answer}{Colors.END}")
            
            print(f"{Colors.BLUE}Puntos este minijuego: {spelling_score}{Colors.END}")
            time.sleep(1.5)
        
        # Resultado final
        self.clear_screen()
        self.print_header()
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}🏁 ¡MINIJUEGO TERMINADO! 🏁{Colors.END}\n")
        print(f"{'━'*60}")
        print(f"🐝 RESULTADOS - SPELLING BEE 🐝")
        print(f"{'━'*60}\n")
        
        print(f"Palabras correctas: {Colors.GREEN}{spelling_correct}/{spelling_rounds}✅{Colors.END}")
        print(f"Puntuación del minijuego: {Colors.BOLD}{Colors.GREEN}{spelling_score} PUNTOS{Colors.END}\n")
        
        accuracy = (spelling_correct / spelling_rounds) * 100
        
        if accuracy == 100:
            print(f"{Colors.GREEN}🌟 ¡CAMPEÓN DE DELETREO! 🌟{Colors.END}")
        elif accuracy >= 80:
            print(f"{Colors.GREEN}🎯 ¡Excelente deletreo! 🎯{Colors.END}")
        elif accuracy >= 60:
            print(f"{Colors.YELLOW}💪 ¡Buen intento! Sigue practicando. 💪{Colors.END}")
        else:
            print(f"{Colors.BLUE}📚 Practica el deletreo en inglés. 📚{Colors.END}")
        
        # Agregar puntos al total
        self.score += spelling_score
        print(f"\n{Colors.GREEN}Los {spelling_score} puntos se han añadido a tu puntuación total!{Colors.END}")
        print(f"{Colors.BLUE}Puntuación acumulada: {self.score}{Colors.END}\n")
        
        print(f"{'─'*60}")
        input(f"{Colors.YELLOW}Presiona ENTER para volver al menú...{Colors.END}")
    
    def play_memory_match_minigame(self):
        """Minijuego Memory Match - Emparejar palabras en español e inglés"""
        self.clear_screen()
        self.print_header()
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}🧠 MINIJUEGO: MEMORY MATCH 🧠{Colors.END}")
        print(f"{Colors.YELLOW}¡Emparea palabras en español con su traducción en inglés!{Colors.END}\n")
        
        print(f"{Colors.BLUE}📋 REGLAS:{Colors.END}")
        print("1. Se te mostrarán palabras en español y sus traducciones")
        print("2. Debes emparejar cada palabra con su traducción correcta")
        print("3. 8 pares de palabras")
        print(f"\nPuntuación: 15 puntos por pareja correcta\n")
        
        input(f"{Colors.YELLOW}Presiona ENTER para comenzar...{Colors.END}")
        
        memory_score = 0
        memory_correct = 0
        memory_rounds = 8
        all_words = list(WORDS_DATABASE.items())
        selected_words = random.sample(all_words, min(memory_rounds, len(all_words)))
        
        # Crear opciones incorrectas
        all_english_words = [data["english"] for _, data in selected_words]
        
        for idx, (spanish, data) in enumerate(selected_words, 1):
            correct_english = data["english"]
            
            # Crear opciones con una respuesta correcta y 3 incorrectas
            wrong_options = random.sample(
                [w for w in all_english_words if w != correct_english], 
                min(3, len(all_english_words) - 1)
            )
            options = [correct_english] + wrong_options
            random.shuffle(options)
            
            self.clear_screen()
            print(f"{Colors.CYAN}{Colors.BOLD}🧠 MEMORY MATCH 🧠{Colors.END}")
            print(f"Ronda {idx}/{memory_rounds}\n")
            
            print(f"{Colors.YELLOW}Palabra en español:{Colors.END}")
            print(f"{Colors.BOLD}{Colors.BLUE}{spanish.upper()}{Colors.END}\n")
            
            print(f"{Colors.YELLOW}¿Cuál es su traducción al inglés?{Colors.END}\n")
            for i, option in enumerate(options, 1):
                print(f"{i}. {option}")
            
            while True:
                try:
                    choice = input(f"\n{Colors.YELLOW}Selecciona la opción (1-4): {Colors.END}").strip()
                    if choice in ["1", "2", "3", "4"]:
                        selected_option = options[int(choice) - 1]
                        break
                    else:
                        print(f"{Colors.RED}Por favor, ingresa un número del 1 al 4.{Colors.END}")
                except:
                    print(f"{Colors.RED}Entrada no válida.{Colors.END}")
            
            # Verificar respuesta
            if selected_option == correct_english:
                memory_correct += 1
                memory_score += 15
                print(f"\n{Colors.GREEN}✅ ¡CORRECTO! +15 puntos{Colors.END}")
            else:
                print(f"\n{Colors.RED}❌ ¡INCORRECTO!{Colors.END}")
                print(f"{Colors.YELLOW}La respuesta correcta era: {correct_english}{Colors.END}")
                print(f"{Colors.RED}Seleccionaste: {selected_option}{Colors.END}")
            
            print(f"{Colors.BLUE}Puntos este minijuego: {memory_score}{Colors.END}")
            time.sleep(1.5)
        
        # Resultado final
        self.clear_screen()
        self.print_header()
        
        print(f"\n{Colors.CYAN}{Colors.BOLD}🏁 ¡MINIJUEGO TERMINADO! 🏁{Colors.END}\n")
        print(f"{'━'*60}")
        print(f"🧠 RESULTADOS - MEMORY MATCH 🧠")
        print(f"{'━'*60}\n")
        
        print(f"Parejas correctas: {Colors.GREEN}{memory_correct}/{memory_rounds}✅{Colors.END}")
        print(f"Puntuación del minijuego: {Colors.BOLD}{Colors.GREEN}{memory_score} PUNTOS{Colors.END}\n")
        
        accuracy = (memory_correct / memory_rounds) * 100
        
        if accuracy == 100:
            print(f"{Colors.GREEN}🌟 ¡MEMORIA PERFECTA! ¡Eres increíble! 🌟{Colors.END}")
        elif accuracy >= 80:
            print(f"{Colors.GREEN}🎯 ¡Excelente memoria! 🎯{Colors.END}")
        elif accuracy >= 60:
            print(f"{Colors.YELLOW}💪 ¡Buen trabajo! Sigue mejorando. 💪{Colors.END}")
        else:
            print(f"{Colors.BLUE}📚 Practica más para mejorar tu memoria. 📚{Colors.END}")
        
        # Agregar puntos al total
        self.score += memory_score
        print(f"\n{Colors.GREEN}Los {memory_score} puntos se han añadido a tu puntuación total!{Colors.END}")
        print(f"{Colors.BLUE}Puntuación acumulada: {self.score}{Colors.END}\n")
        
        print(f"{'─'*60}")
        input(f"{Colors.YELLOW}Presiona ENTER para volver al menú...{Colors.END}")
    
    def run(self):
        """Loop principal del juego"""
        while True:
            self.show_menu()
            
            try:
                choice = input(f"{Colors.YELLOW}Selecciona una opción (1-8): {Colors.END}").strip()
                
                if choice == "1":
                    self.play_game(1)
                elif choice == "2":
                    self.play_game(2)
                elif choice == "3":
                    self.play_game(3)
                elif choice == "4":
                    self.play_flash_words_minigame()
                elif choice == "5":
                    self.play_spelling_bee_minigame()
                elif choice == "6":
                    self.play_memory_match_minigame()
                elif choice == "7":
                    self.show_stats()
                elif choice == "8":
                    self.clear_screen()
                    print(f"\n{Colors.CYAN}{Colors.BOLD}👋 ¡Gracias por jugar! 👋{Colors.END}\n")
                    print(f"{Colors.YELLOW}Puntuación final: {self.score} puntos{Colors.END}\n")
                    sys.exit(0)
                else:
                    print(f"{Colors.RED}❌ Opción no válida. Intenta de nuevo.{Colors.END}")
                    time.sleep(1.5)
            
            except KeyboardInterrupt:
                print(f"\n\n{Colors.CYAN}👋 ¡Hasta luego!{Colors.END}\n")
                sys.exit(0)
            except Exception as e:
                print(f"{Colors.RED}❌ Error: {str(e)}{Colors.END}")
                time.sleep(1.5)

def main():
    """Función principal"""
    try:
        game = PronunciationGame()
        game.run()
    except Exception as e:
        print(f"{Colors.RED}Error fatal: {str(e)}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
