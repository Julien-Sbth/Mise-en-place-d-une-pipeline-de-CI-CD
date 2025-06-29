# 🛠️ Pipeline CI/CD Python + Docker avec GitHub Actions

![CI](https://github.com/Hamdoune001/pipeline_ci_cd/actions/workflows/python-app.yml/badge.svg)

Ce projet est un exemple d'intégration continue (CI) simple en Python.  
Il intègre des tests unitaires, une vérification de qualité du code avec `pylint`, et un build d'image Docker exécutant les tests automatiquement.

---

## 📁 Contenu du projet

- `python.py` : contient une classe `SimpleMath` avec des fonctions `addition` et `soustraction` ainsi que des test unitaires avec `unittest`.
---

## ⚙️ Fonctionnalités CI/CD

Le workflow GitHub Actions effectue automatiquement à chaque `push` :

1. ✅ **Exécution des tests unitaires**
2. ✅ **Analyse statique du code avec `pylint`**
3. ✅ **Build d'un conteneur Docker**
4. ✅ **Exécution des tests dans le conteneur**

---

---

## 🐳 Docker

Une image Docker est construite automatiquement dans le pipeline.  
Lorsqu'on exécute le conteneur, les tests unitaires sont automatiquement lancés grâce à la directive :

```Dockerfile
CMD ["python3", "test_simple_math.py"]
