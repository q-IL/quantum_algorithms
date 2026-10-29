# Lorenz 96 et méthodes quantiques

Deux notebooks écrits pendant la finale du hackathon quantique organisé par le CERFACS à Toulouse les 26,27 et 28 octobre 2026. Ils abordent le système chaotique de Lorenz 96 sous deux angles : prévoir sa trajectoire avec un réservoir quantique, et calculer sa moyenne d'ensemble avec un algorithme quantique de type Kolmogorov. Tout est simulé classiquement (Qiskit, vecteurs d'état), sans exécution sur du matériel réel.

Ce sujet a été écrit par les membres de Quobly. Notre équipe, composée de Victor LAMARCHE, Adrien COUSIN-FRESSINET et moi-même, a pu obtenir la deuxième place du Hackathon.

Les notebook ont peu été retouchés a posteriori. Nous vous prions de nous excuser si ils manquent de clareté

| Notebook | Sujet |
|---|---|
| [`QRC.ipynb`](QRC.ipynb) | Quantum Reservoir Computing pour prévoir Lorenz 96 |
| [`kolmogorian_lorenz96_challenge.ipynb`](kolmogorian_lorenz96_challenge.ipynb) | Prévision d'ensemble d'un Lorenz 96 stochastique par l'algorithme de Bravyi et al. |

## 1. `QRC.ipynb` : Quantum Reservoir Computing

Cette méthode nous a été proposée par Romain Logean (Quobly). Nous le remercions chaleureusement pour ses conseils.

**Principe.** Les 8 variables de Lorenz 96 (F = 8, régime chaotique) sont encodées par des rotations RY dans un circuit de 8 qubits. Un paramètre `I ∈ [0, 1]` règle l'intrication, de l'anneau de CNOT (`I = 0`) à toutes les paires (`I = 1`). Les 2⁸ probabilités de sortie servent de features à une régression ridge, puis la prévision se fait en boucle fermée.

**Contenu.**
-Réalisation d'un Quantum Extreme Machine Learning (QEML)
- Générateur de circuits paramétrés (`build_circuit`) : intrication `I`, couches d'encodage, seeds reproductibles.
- Recherche d'hyperparamètres (`I` : l'intrication du réservoir, échelle d'encodage `lam`, régularisation `ridge_alpha`) et analyse d'une optimisation des prédictions ainsi fournies via le temps de validité.
- Comparaison du QEML avec un « vrai » QRC à mémoire, par mélange `r_t = (1-ε) r_{t-1} + ε f(u_t)`.

**Résultats.** Le temps de prévision valide (erreur normalisée < 0,5) atteint environ 8 à 15 temps de Lyapunov selon `I` et la graine. Le mélange ε = 0,15 n'apporte pas de gain net par rapport à la version sans mémoire.

**Warning** les temps de de validité (unités de temps de Lyapunov) semblent très grands comparés à la littérature et le système pas assez chaotique à ces échelles. Il serait bon de revoir la normalisation (piste : `dt_out` vs pas de temps). La comparaison entre deux courbes reste correcte.

## 2. `kolmogorian_lorenz96_challenge.ipynb` : algorithme de Kolmogorov

Ce notebook est une version modifiée et complétée du notebook initialement en anglais fourni par notre mentor Karla Baumann (Quobly). Les parties et notes en français sont les notres. Nous la remercions coridialement pour ses précieuses expliquations.

**Principe.** Pour un Lorenz 96 stochastique (K = 4, λ = 1, q = 2), la moyenne d'ensemble `E[X₁(t)]` obéit à une équation de Kolmogorov rétrograde linéaire. En base de Hermite (oscillateur harmonique), elle devient `dψ/dt = (−Λ + C) ψ` avec `C` antihermitienne. On décompose `C` en chaînes de Pauli, on applique Trotter, puis on construit le circuit avec Qiskit. L'amortissement `Λ` est appliqué classiquement (non réalisable en paratique ou sans avantage, uniquement fait pour comparer les résulats théoriques) ou par block-encoding avec post-sélection. Le tout est comparé à un Monte Carlo.

**Résultats** (condition initiale fixe, comparaison au Monte Carlo) :
- L'émulateur exact avec d = 4 (8 qubits) est cohérent avec le Monte Carlo à moins de 3 erreurs standard.
- L'erreur de Trotter est d'ordre 1 : elle est divisée par ~2 quand on double le nombre de pas (1,5·10⁻² à 1,1·10⁻³ de 4 à 64 pas).
- Le block-encoding reproduit la version classique à ~10⁻¹⁵ mais nécéssite un nombre important de mesures.
- L'erreur résiduelle vient surtout de la troncature : l'écart moyen au Monte Carlo plafonne à ~0,035 pour d = 2 (4 qubits) et tombe à ~0,017 pour d = 4.

**Non traité.** Le Stage 4 (bruit des qubits de spin avec SpinPulse).

**Piste d'avancement** Ici le résultat est obtenu via Qiskit et le state-vector. Ceci n'est pas possible en pratique. Il faut ou bien réaliser plusieurs passages (et mesures) pour estimer l'état de sortie, ou bien faire en sorte que mettre en place une méthode de d'estimation de la moyenne par test de Hadamard

> L'énoncé, la boîte à outils et la référence Monte Carlo viennent des organisateurs ; les fonctions des stages 1 à 3 sont les nôtres.

## Installation

```bash
pip install numpy scipy matplotlib scikit-learn qiskit spin-pulse
```

`spin-pulse` n'est importé que par le second notebook.

## Références

- Bravyi, Manson-Sawko, Zayats, Zhuk, *Quantum simulation of a noisy classical nonlinear dynamics*, arXiv:2507.06198 (2025)
- Bravyi, Byrne, Zayats, Zhuk, *Quantum algorithms for stochastic nonlinear differential equations*, arXiv:2606.08349 (2026)

## Auteurs

Iohannès Laurent, Victor Lamarche, Adrien Cousin-Fressinet.
