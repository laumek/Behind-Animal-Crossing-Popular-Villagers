# acnh-villager-popularity-data-analysis


**Analysing Trends with Data & Machine Learning**

Do real-world biases shape how we rank Animal Crossing villagers? This project explores whether traits like species, personality, and gender influence villager popularity — and how our perceptions of cuteness, rarity, and friendliness affect in-game preferences.

## About the Data

* **413 villagers** (214 males, 199 females)
* Features: Name, Rank, Tier (1–6), Species (36 types), Gender, Personality (16 types)

## Key Insights

* **Species** has the strongest influence on popularity (ε² ≈ 0.27, large effect)
  → "Cuter" species (cats, deer, octopuses) rank higher; bolder-looking ones (hippos, bulls, gorillas) rank lower
* **Personality** has a moderate effect (ε² ≈ 0.09)
  → Friendlier personalities (Peppy, Lazy, Big Sister) are preferred over aloof/grumpy types (Cranky, Snooty)
* **Gender** shows no significant impact

## Methods

* Exploratory Data Analysis (EDA)
* Kruskal-Wallis test (+ epsilon-squared squared) + Dunn’s post hoc test
* Visualization of trends in species, personality, and gender distributions

## Why it matters

This analysis reveals how cultural aesthetics and social biases subtly shape even whimsical virtual spaces. Patterns in villager popularity reflect familiar standards of appeal — from neoteny and kawaii culture to rarity and exclusivity dynamics.

## Repository contents

* **Data retrieval** (APIs)
* **EDA notebook** (analysis + visualizations)
