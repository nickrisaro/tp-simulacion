from Ejercicio04 import generar_random_array_estandar_aceptados
from scipy.stats import kstest

SIGNIFICANCIA_KS = 0.01

def main():
    print("7) Aplicar el test de Kolmogorov-Smirnov al generador de numeros al azar generado en el ejercicio 4.")
    print("Analizar el resultado del mismo, e indicar si la distribucion puede o no ser aceptada.")
    print("Considerar un nivel de significacion del 1%.")

    ks_test_result = kstest(generar_random_array_estandar_aceptados(), 'norm')

    print("El p valor es", ks_test_result.pvalue)

    if ks_test_result.pvalue < SIGNIFICANCIA_KS:
        print("Se rechaza H0 (siendo H0 que la distribucion es normal")
    else:
        print("Se acepta H0")

if __name__ == "__main__":
    main()