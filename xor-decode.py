#!/usr/bin/env python3

import argparse
import base64
import sys


# ============================================================
# COLORES ANSI
# ============================================================

RESET = "\033[0m"

BOLD = "\033[1m"

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"
GRAY = "\033[90m"


XOR_KEY = 0x5F


# ============================================================
# FUNCIONES VISUALES
# ============================================================

def banner():
    print(f"""
{CYAN}{BOLD}
╔════════════════════════════════════════════════════════════╗
║                                                            ║
║                  XOR DECODER - {xor_title()}                ║
║                                                            ║
║              Base64 + XOR 0x5F Decoder                    ║
║                                                            ║
╚════════════════════════════════════════════════════════════╝
{RESET}
""")


def xor_title():
    return "{xor}"


def separator():
    print(f"{GRAY}{'─' * 60}{RESET}")


def print_step(number, title, description=None):
    print()
    print(
        f"{CYAN}{BOLD}"
        f"┌─[ PASO {number} ] {title}"
        f"{RESET}"
    )

    separator()

    if description:
        print(f"{WHITE}{description}{RESET}")


def print_value(label, value, color=YELLOW):
    print(f"    {GRAY}{label:<15}{RESET}: {color}{value}{RESET}")


# ============================================================
# DECODIFICACIÓN
# ============================================================

def decode_xor(value, verbose=True):

    value = value.strip()

    # --------------------------------------------------------
    # PASO 1 - Valor recibido
    # --------------------------------------------------------

    if verbose:
        print_step(
            1,
            "Valor recibido",
            "El usuario proporciona el valor que contiene el prefijo "
            "{xor} y la cadena codificada."
        )

        print_value("Entrada", value)

    # --------------------------------------------------------
    # PASO 2 - Comprobar {xor}
    # --------------------------------------------------------

    if not value.startswith("{xor}"):
        raise ValueError(
            "El valor proporcionado no comienza con el prefijo {xor}."
        )

    encoded = value[5:]

    if verbose:
        print_step(
            2,
            "Eliminar el prefijo {xor}",
            "El prefijo {xor} identifica el formato utilizado. "
            "Se elimina para trabajar con la cadena Base64."
        )

        print_value("Antes", value, YELLOW)
        print_value("Después", encoded, GREEN)

    # --------------------------------------------------------
    # PASO 3 - Base64
    # --------------------------------------------------------

    try:
        decoded = base64.b64decode(
            encoded,
            validate=True
        )

    except Exception:
        raise ValueError(
            "La cadena restante no es un Base64 válido."
        )

    if verbose:
        print_step(
            3,
            "Decodificar Base64",
            "La cadena restante se decodifica utilizando Base64. "
            "El resultado todavía NO es la contraseña."
        )

        print_value(
            "Base64",
            encoded,
            YELLOW
        )

        print_value(
            "Bytes",
            decoded,
            GREEN
        )

        print_value(
            "Hexadecimal",
            decoded.hex(),
            MAGENTA
        )

    # --------------------------------------------------------
    # PASO 4 - XOR
    # --------------------------------------------------------

    result = bytes(
        byte ^ XOR_KEY
        for byte in decoded
    )

    if verbose:
        print_step(
            4,
            "Aplicar XOR",
            "Cada byte obtenido anteriormente se combina mediante "
            f"XOR utilizando la clave 0x{XOR_KEY:02X}."
        )

        print_value(
            "Clave XOR",
            f"0x{XOR_KEY:02X}",
            YELLOW
        )

        print_value(
            "Entrada",
            decoded.hex(),
            MAGENTA
        )

        print_value(
            "Resultado",
            result.hex(),
            GREEN
        )

    # --------------------------------------------------------
    # PASO 5 - UTF-8
    # --------------------------------------------------------

    try:
        plaintext = result.decode("utf-8")

    except UnicodeDecodeError:
        raise ValueError(
            "El resultado del XOR no puede convertirse a texto UTF-8."
        )

    if verbose:
        print_step(
            5,
            "Convertir a texto plano",
            "Los bytes resultantes del XOR se interpretan como "
            "texto UTF-8."
        )

        print_value(
            "Texto plano",
            plaintext,
            GREEN
        )

    return plaintext


# ============================================================
# AYUDA
# ============================================================

def show_examples():

    banner()

    print(f"{CYAN}{BOLD}EJEMPLOS DE USO{RESET}")
    separator()

    print(f"""
{WHITE}1. Modo interactivo:{RESET}

    {GREEN}python3 xor_decoder.py{RESET}

    El programa solicitará:

    {GRAY}Introduce el valor {{xor}}:{RESET}

    {YELLOW}{{xor}}Oz4rPj0+LDovPiwsKDAtOw=={RESET}


{WHITE}2. Pasar el valor directamente:{RESET}

    {GREEN}python3 xor_decoder.py \
"{{xor}}Oz4rPj0+LDovPiwsKDAtOw=="{RESET}


{WHITE}3. Mostrar ayuda:{RESET}

    {GREEN}python3 xor_decoder.py --help{RESET}


{WHITE}4. Mostrar ejemplos:{RESET}

    {GREEN}python3 xor_decoder.py --examples{RESET}


{CYAN}{BOLD}PROCESO DE DECODIFICACIÓN{RESET}
{GRAY}────────────────────────────────────────────────────────────{RESET}

    {YELLOW}{{xor}} + Base64{RESET}
           │
           ▼
    {BLUE}Eliminar {{xor}}{RESET}
           │
           ▼
    {BLUE}Decodificar Base64{RESET}
           │
           ▼
    {BLUE}Aplicar XOR 0x5F{RESET}
           │
           ▼
    {GREEN}Convertir a texto UTF-8{RESET}
           │
           ▼
    {GREEN}{BOLD}Texto plano{RESET}
""")


# ============================================================
# MODO INTERACTIVO
# ============================================================

def interactive_mode():

    banner()

    print(
        f"{WHITE}"
        "Herramienta educativa para decodificar valores "
        "con formato {xor}."
        f"{RESET}"
    )

    print()
    print(
        f"{GRAY}Escriba 'exit' o 'quit' para salir."
        f"{RESET}"
    )

    print(
        f"{GRAY}Escriba 'help' para mostrar la ayuda."
        f"{RESET}"
    )

    while True:

        try:

            print()
            value = input(
                f"{CYAN}{BOLD}"
                "┌──[ Introduce el valor {xor} ]\n"
                "└─> "
                f"{RESET}"
            ).strip()

            # ------------------------------------------------
            # Salir
            # ------------------------------------------------

            if value.lower() in ("exit", "quit"):

                print(
                    f"\n{GREEN}[+] Saliendo...{RESET}\n"
                )

                break

            # ------------------------------------------------
            # Ayuda
            # ------------------------------------------------

            if value.lower() in ("help", "?"):

                show_examples()
                continue

            # ------------------------------------------------
            # Entrada vacía
            # ------------------------------------------------

            if not value:

                print(
                    f"{RED}"
                    "[-] No se introdujo ningún valor."
                    f"{RESET}"
                )

                continue

            # ------------------------------------------------
            # Iniciar proceso
            # ------------------------------------------------

            print()

            print(
                f"{MAGENTA}{BOLD}"
                "╔══════════════════════════════════════════════════════════╗"
                "║          INICIANDO DECODIFICACIÓN                      ║"
                "╚══════════════════════════════════════════════════════════╝"
                f"{RESET}"
            )

            # ------------------------------------------------
            # Decodificar
            # ------------------------------------------------

            plaintext = decode_xor(value)

            # ------------------------------------------------
            # Resultado final
            # ------------------------------------------------

            print()

            print(
                f"{GREEN}{BOLD}"
                "╔══════════════════════════════════════════════════════════╗"
                "║              DECODIFICACIÓN COMPLETADA                 ║"
                "╚══════════════════════════════════════════════════════════╝"
                f"{RESET}"
            )

            print()

            print(
                f"    {WHITE}{BOLD}"
                "Texto plano"
                f"{RESET}"
                f" : {GREEN}{BOLD}{plaintext}{RESET}"
            )

        except KeyboardInterrupt:

            print(
                f"\n\n{GREEN}[+] Saliendo...{RESET}\n"
            )

            break

        except Exception as error:

            print()

            print(
                f"{RED}{BOLD}"
                "╔══════════════════════════════════════════════════════════╗"
                "║                       ERROR                             ║"
                "╚══════════════════════════════════════════════════════════╝"
                f"{RESET}"
            )

            print(
                f"\n    {RED}[-] {error}{RESET}"
            )

            print(
                f"    {GRAY}"
                "Comprueba que el valor tenga el formato correcto."
                f"{RESET}"
            )


# ============================================================
# ARGUMENTOS
# ============================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Decodificador de valores con formato "
            "{xor} + Base64 + XOR."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Ejemplos:

  Modo interactivo:
    python3 xor_decoder.py

  Valor directo:
    python3 xor_decoder.py "{xor}Oz4rPj0+LDovPiwsKDAtOw=="

  Ejemplos:
    python3 xor_decoder.py --examples
"""
    )

    parser.add_argument(
        "value",
        nargs="?",
        help="Valor {xor} que se desea decodificar."
    )

    parser.add_argument(
        "--examples",
        action="store_true",
        help="Mostrar ejemplos y explicación del proceso."
    )

    args = parser.parse_args()

    # --------------------------------------------------------
    # --examples
    # --------------------------------------------------------

    if args.examples:

        show_examples()
        return

    # --------------------------------------------------------
    # Valor proporcionado como argumento
    # --------------------------------------------------------

    if args.value:

        banner()

        try:

            plaintext = decode_xor(args.value)

            print()

            print(
                f"{GREEN}{BOLD}"
                "╔══════════════════════════════════════════════════════════╗"
                "║              DECODIFICACIÓN COMPLETADA                 ║"
                "╚══════════════════════════════════════════════════════════╝"
                f"{RESET}"
            )

            print(
                f"\n    {WHITE}{BOLD}"
                f"Texto plano"
                f"{RESET} : {GREEN}{BOLD}{plaintext}{RESET}\n"
            )

        except Exception as error:

            print(
                f"\n{RED}[-] Error: {error}{RESET}\n"
            )

            sys.exit(1)

    # --------------------------------------------------------
    # Sin argumentos -> modo interactivo
    # --------------------------------------------------------

    else:

        interactive_mode()


if __name__ == "__main__":
    main()
