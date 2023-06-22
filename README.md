
# Otimização Combinatória: Problema do Caixeiro Viajante :compass:


- [Definições](#def)
- [Metodologia](#instrument)
- [Resultados](#result)

 <details>
<summary id ="def"><h2><strong>1 - Definições</strong></h2></summary>

---
O problema TSP é um problema cássico de inteligência computacional, do tipo N p-difícil. \
A implementação da heurística **deve** ser adaptada, de modo a se tratar de um problema combinatório sem repetições.  

O problema é levantado no trabalho conhecido como TSPLib [^1] e possui diversos *rotas*, cada um com diversas *subrotas*, em variadas dimensões (simples, médias e as mais complexas). \
Lá, propõem formas de distância entre as *cidades* baseados na distância Euclidiana. Outros seguem distâncias ponderadas e outros utilizam baseam-se na distância geométrica. \
Para os exemplos deste repositório foram trabalhadas apenas as distâncias Euclidianas, e a distância ponderada (problemas ATSP). \
O problema TSP com distância Euclidiana utiliza a seguinte definição de distância entre cidades:

```math
  d(\mathbf{p}, \mathbf{q}) = \sqrt{\sum_{i=1}^{n} (q_i - p_i)^2}
```
Já o problema ATSP trabalha com a distância em formato matricial (diagonais *dont-care*), onde a distância de uma n-ésima cidade vale: 

```math
d_{nm}=
\begin{bmatrix}
999999 & a_{12} & a_{13} & \dots & a_{1n} \\
a_{21} & 999999 & a_{23} & \dots & a_{2n} \\
a_{31} & a_{32} & 999999 & \dots & a_{3n} \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
a_{n1} & a_{n2} & a_{n3} & \dots & 999999 \\
\end{bmatrix}
```

 </details>
 <!-- ################################################################2#################################################### -->
<details>
 <summary id="instrument"> <h2> <strong>2 - Metodologia </h2> </strong> </summary>
 
---
- Importação dos arquivos .txt,
  - RunTSP.py para arquivos TSP.  
  - RunATSP.py para arquivos ATSP.
  
- Uso da biblioteca *PYGad* para algoritmo genético [^2],
- Implementações dos operadores personalizados:
    - Problema com não-repetição nos genes, operadores implementados (cross-over e mutação por inverão [^4]).
- Execução individual com orçamento computacional (n de execuções):
  - **Se** D<50: 50000.
  - **Se-não**: 70000.
- **Fim**: Traçar a curva de aprendizado geração a geração.


</details>
<!-- ################################################################2#################################################### -->
<details>
 <summary id="result"> <h2> <strong>3- Resultados </h2> </strong> </summary>

Os problemas de ordem menor apresentaram erro relativo baixo:

| | B52  | Ch130 | Br17  | Ftv70 |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| **Obtido**  | 8303  | 9560  | 39  | 2439  |
| **Ótimo** | 7542 | 6110 | 39  | 1950 |
| **Erro rel. (%)**  | 9.2  | 56 | 0  | 25  |

O tempo de uma execução foi de 2 minutos para o B52 enquanto Ch130 cerca de 10 minutos. \
Os resultados que apresentaram um erro relativo elevado (principalmente o Ch130) será tratado neste repositório, futuramente, com meta-herísticas mais apropriadas. 

</details>

[^1]: Instâncias do problema, resultados ótimos e temas relacionados. [Site institucional Universitàt Heindelberg](http://comopt.ifi.uni-heidelberg.de/software/)  
[^2]: Documentação da biblioteca [PYGAD](https://pygad.readthedocs.io/en/latest/README_pygad_ReadTheDocs.html).

[^3]: Network NX.

[^4]: Operador de mutação 'Inverted Mutation':[International Journal of Combinatorial Optimization Problems and Informatics](https://www.redalyc.org/pdf/2652/265219635002.pdf)

