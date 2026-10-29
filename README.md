# UrbanSolar Battery - Fork personnel de test

![Intégration HACS](https://img.shields.io/badge/HACS-Int%C3%A9gration-blue?logo=home-assistant)
![Plateforme Home Assistant](https://img.shields.io/badge/Plateforme-Home%20Assistant-41BDF5?logo=home-assistant)
![Statut : fork de test](https://img.shields.io/badge/Statut-Fork%20de%20test-orange)

> **Avis :** ce fork personnel de test n'est ni affilié au projet d'origine ni pris en charge par celui-ci. Il est fourni « en l'état », sans assistance ni garantie.

---

## 📚 Sommaire

1. [Ajouter le dépôt HACS](#ajouter-le-depot-hacs)
2. [Installer l'intégration](#installer-lintegration)
3. [Configuration](#configuration)
4. [Entités & Automatisations](#entites-et-automatisations)
5. [Tableau de bord Lovelace](#tableau-de-bord-lovelace)
6. [Dépannage](#depannage)
7. [À propos de ce fork](#a-propos-de-ce-fork)

---

<a id="ajouter-le-depot-hacs"></a>
## 1. Ajouter le dépôt HACS

La version de test publiée actuellement est [Urban Solar Battery 1.0.2](https://github.com/BeletteHome/ha-urbansolar-bv/releases/tag/v1.0.2). Le contrôle HACS du dépôt échoue actuellement sur les métadonnées GitHub : licence absente, fonctionnalité de signalement désactivée et sujets du dépôt manquants. L'installation manuelle de l'archive ZIP reste disponible ci-dessous.

1. Ouvrez **HACS** dans Home Assistant.  
2. Allez dans l’onglet **Intégrations**.  
3. Cliquez sur **➕ Ajouter un dépôt personnalisé** et entrez l’URL :  
  `https://github.com/BeletteHome/ha-urbansolar-bv`
4. Sélectionnez **Catégorie : Intégration**.  
5. Cliquez sur **Enregistrer**.

---

<a id="installer-lintegration"></a>
## 2. Installer l'intégration

Avant toute installation ou mise à jour, créez une sauvegarde Home Assistant. N'exécutez pas simultanément le dépôt d'origine et ce fork : ils utilisent le même domaine et les mêmes fichiers de configuration. Lors d'un remplacement manuel, conservez l'entrée d'intégration et les fichiers `urban_*.yaml` existants.

### Installation manuelle de la version 1.0.2

1. Téléchargez l'archive [`urbansolar_bv.zip`](https://github.com/BeletteHome/ha-urbansolar-bv/releases/download/v1.0.2/urbansolar_bv.zip) depuis la page de la publication.
2. Si une ancienne version est installée, arrêtez Home Assistant et supprimez ou déplacez uniquement son ancien dossier de code dans `custom_components/`. Ne supprimez ni l'entrée d'intégration dans Home Assistant ni les fichiers `urban_*.yaml`.
3. Créez le dossier `/config/custom_components/ha_urbansolar_bv/`, puis décompressez-y le contenu de l'archive. Vérifiez que `manifest.json` se trouve directement dans ce dossier, et non dans un sous-dossier supplémentaire.
4. Redémarrez Home Assistant.
5. Dans **Paramètres → Appareils et services**, vérifiez l'entrée **UrbanSolar Battery**. Si c'est une nouvelle installation, choisissez **Ajouter une intégration** et sélectionnez les capteurs source à l'étape suivante.

Pour une installation HACS, utilisez le dépôt personnalisé de la section 1, sélectionnez **UrbanSolar Battery 1.0.2**, puis redémarrez Home Assistant. Comme ce dépôt échoue actuellement à certains contrôles HACS, l'installation manuelle est le parcours de test recommandé.

Les cartes Lovelace ci-dessous ne sont pas nécessaires au fonctionnement de l'intégration. Installez-les uniquement si vous souhaitez utiliser le tableau de bord fourni.

### 📦 Dépendances Lovelace requises

L’intégration utilise plusieurs cartes Lovelace que vous devez installer via HACS :

| Carte Lovelace              | Dépôt GitHub                                                   |
|----------------------------|----------------------------------------------------------------|
| ApexCharts Card            | [apexcharts-card](https://github.com/RomRider/apexcharts-card) |
| Vertical Stack In Card     | [vertical-stack-in-card](https://github.com/custom-cards/vertical-stack-in-card) |
| Number Box Card            | [numberbox-card](https://github.com/junkfix/numberbox-card) | 
| Energy Flow Card Plus      | [energy-flow-card-plus](https://github.com/flixlix/energy-flow-card-plus) |
| Power Flow Card Plus       | [power-flow-card-plus](https://github.com/flixlix/power-flow-card-plus) |

> **N'oubliez pas de redémarrer Home Assistant** après installation.

---

<a id="configuration"></a>
## 3. Configuration

Lors de l’ajout de l’intégration, une boîte de dialogue vous demandera de sélectionner :

1. **Capteur de puissance totale consommée** (ex : `sensor.puissance_totale_consommee`)  
2. **Capteur de puissance solaire produite** (ex : `sensor.pv_energie_solaire`)

> **Important :** les deux entités doivent être des capteurs de puissance (`device_class: power`) dont l'unité est exactement `kW`. Les valeurs sont converties en watts par l'intégration. Les capteurs configurés uniquement en `W` ne passent pas la validation actuelle.

Si la boîte de dialogue ne s’affiche pas : **Paramètres → Appareils et services → Ajouter une intégration → UrbanSolar Battery**.

Après la première configuration de l'intégration, celle-ci copie ses fichiers YAML dans `/config`. Ajoutez les inclusions nécessaires à votre `configuration.yaml` (ne dupliquez pas une clé de premier niveau déjà présente) :

```yaml
# Urban Solar Battery
input_number: !include urban_input_numbers.yaml
sensor: !include urban_integrations.yaml
template: !include urban_sensors.yaml
utility_meter: !include urban_utility_meters.yaml
```

Pour les automations, Home Assistant n'accepte qu'une seule clé `automation:` de premier niveau. Si vous n'avez pas déjà d'inclusion d'automations, vous pouvez ajouter :

```yaml
automation: !include urban_automations.yaml
```

Si votre configuration utilise déjà `automation:`, ne créez pas une deuxième clé. Pour charger plusieurs listes YAML, placez vos fichiers d'automations, ainsi que le contenu de `urban_automations.yaml`, dans un dossier `automations/`, puis utilisez une seule déclaration :

```yaml
automation: !include_dir_merge_list automations/
```

Les automations gérées par l'interface Home Assistant sont stockées séparément. Après modification de `configuration.yaml`, vérifiez la configuration et redémarrez Home Assistant.

L'intégration copie `urban_dashboard.yaml` dans `/config`, mais ne crée ni n'enregistre automatiquement un tableau de bord Home Assistant. Pour enregistrer ce fichier comme tableau de bord de la barre latérale, ajoutez cette entrée au bloc `lovelace:` existant de `configuration.yaml` :

```yaml
lovelace:
  dashboards:
    urban-solar:
      mode: yaml
      title: Urban Solar
      icon: mdi:solar-power
      show_in_sidebar: true
      filename: urban_dashboard.yaml
```

Redémarrez ensuite Home Assistant. Le contenu complet du fichier `urban_dashboard.yaml` est fourni ci-dessous. Les cartes frontend indiquées dans la section précédente doivent être installées séparément.

```yaml
views:
  - title: Urban
    sections:
      - type: grid
        cards:
          - type: custom:energy-flow-card-plus
            entities:
              battery:
                entity:
                  production: sensor.urban_batterie_virtuelle_entree_horaire
                  consumption: sensor.urban_batterie_virtuelle_sortie_horaire
                state_of_charge: input_number.urban_batterie_virtuelle_stock
                state_of_charge_unit: kwh
                use_metadata: false
              grid:
                entity:
                  consumption: sensor.urban_energie_importee_enedis
                use_metadata: false
              home:
                entity: sensor.urban_energie_consommee_totale
                subtract_individual: false
                use_metadata: false
                override_state: true
              solar:
                entity: sensor.urban_energie_solaire_produite
            clickable_entities: true
            display_zero_lines: true
            use_new_flow_rate_model: true
            energy_date_selection: false
            wh_decimals: 1
            kwh_decimals: 0
            min_flow_rate: 1
            max_flow_rate: 6
            max_expected_energy: 2000
            min_expected_energy: 10
            wh_kwh_threshold: 1000
                title: Flux d'énergie
          - type: custom:apexcharts-card
            graph_span: 3d
            span:
              end: minute
            header:
              show: true
              title: Batterie Virtuelle
              show_states: true
              colorize_states: true
            series:
              - entity: input_number.urban_batterie_virtuelle_stock
                yaxis_id: first
                name: Stock batterie
                type: line
                group_by:
                  duration: 0.5h
                  func: last
                stroke_width: 3
              - entity: input_number.urban_batterie_virtuelle_pointage
                yaxis_id: first
                name: Pointage manuel
                type: line
                stroke_width: 3
                color: '#995000'
                show:
                  in_chart: false
            yaxis:
              - id: first
                decimals: 1
                apex_config:
                  tickAmount: 4
          - type: custom:power-flow-card-plus
            entities:
              battery:
                entity:
                  consumption: sensor.urban_puissance_batterie_virtuelle_out
                  production: sensor.urban_puissance_batterie_virtuelle_in
                state_of_charge: input_number.urban_batterie_virtuelle_stock
                display_state: one_way_no_zero
                state_of_charge_unit: kwh
                show_state_of_charge: true
                use_metadata: true
                color_circle: true
              grid:
                entity: sensor.urban_puissance_import_enedis
                display_state: one_way
                secondary_info: {}
              solar:
                entity: sensor.urban_puissance_solaire_instant
                display_zero_state: true
                secondary_info: {}
              home:
                secondary_info: {}
                entity: sensor.urban_conso_totale_instant
                override_state: true
            clickable_entities: true
            display_zero_lines: true
            use_new_flow_rate_model: true
            w_decimals: 0
            kw_decimals: 1
            min_flow_rate: 0.75
            max_flow_rate: 6
            max_expected_power: 2000
            min_expected_power: 0.01
            watt_threshold: 1000
            transparency_zero_lines: 0
            sort_individual_devices: false
            title: Flux de puissance
          - type: custom:apexcharts-card
            graph_span: 3d
            span:
              end: minute
            header:
              show: true
              title: Bilan energie réseau
              show_states: true
              colorize_states: true
            apex_config:
              chart:
                type: line
            series:
              - entity: sensor.urban_energie_restituee_au_reseau
                yaxis_id: first
                type: line
                color: green
                group_by:
                  duration: 0.5d
                  func: diff
                name: Variation quotidienne
            yaxis:
              - id: first
                decimals: 0
                apex_config:
                  tickAmount: 4
          - type: custom:apexcharts-card
            graph_span: 3day
            span:
              end: minute
            header:
              show: true
              title: Batterie Virtuelle - Flux Horaire
              show_states: true
              colorize_states: true
            apex_config:
              chart:
                type: area
              stroke:
                curve: smooth
            series:
              - entity: input_number.urban_energie_battery_in_hourly
                yaxis_id: first
                name: Entrée Batterie (IN)
                type: line
                color: '#00C853'
                stroke_width: 3
                group_by:
                  duration: 1h
                  func: avg
              - entity: input_number.urban_energie_battery_out_hourly
                name: Sortie Batterie (OUT)
                yaxis_id: first
                type: line
                color: '#D50000'
                stroke_width: 3
                group_by:
                  duration: 1h
                  func: avg
              - entity: sensor.urban_energie_restituee_au_reseau_hourly
                name: Bilan energie
                yaxis_id: second
                type: line
                color: yellow
                stroke_width: 1
                group_by:
                  duration: 1h
                  func: avg
            yaxis:
              - id: first
                decimals: 1
                apex_config:
                  tickAmount: 4
              - id: second
                opposite: true
                decimals: 1
                apex_config:
                  tickAmount: 4
          - type: custom:vertical-stack-in-card
            cards:
              - type: custom:vertical-stack-in-card
                title: Batterie Virtuelle (kWh)
                cards:
                  - type: custom:numberbox-card
                    entity: input_number.urban_batterie_virtuelle_stock
                    name: Stock calculé
                    icon: mdi:battery
                    min: -100
                    max: 200
                    step: 0.1
                    unit: kWh
                    border: false
              - type: entities
                entities:
                  - entity: sensor.urban_energie_restituee_au_reseau_hourly
                    name: Variation horaire
                    icon: mdi:clock-in
                  - entity: sensor.urban_batterie_virtuelle_entree_horaire
                    secondary_info: none
                    name: Entrée batterie (énergie)
                    icon: mdi:battery-arrow-down
                  - entity: sensor.urban_batterie_virtuelle_sortie_horaire
                    name: Sortie batterie (énergie)
                    icon: mdi:battery-arrow-up
                title: Compteurs horaires et bilan
                grid_options:
                  columns: 12
                  rows: 6
                state_color: true
        column_span: 3
      - type: grid
        cards:
          - type: heading
            heading_style: title
        column_span: 2
    cards: []
    type: sections
    max_columns: 3
    dense_section_placement: false

```




<a id="entites-et-automatisations"></a>
## 4. Entités & Automatisations

### Capteurs créés automatiquement

| Entité | Rôle |
|--------|------|
| `sensor.urban_puissance_import_enedis` | Puissance importée du réseau, en W |
| `sensor.urban_puissance_batterie_virtuelle_in` | Puissance dirigée vers la batterie virtuelle, en W |
| `sensor.urban_puissance_batterie_virtuelle_out` | Puissance fournie par la batterie virtuelle, en W |
| `sensor.urban_puissance_solaire_instant` | Puissance solaire instantanée, en W |
| `sensor.urban_conso_totale_instant` | Puissance totale consommée, en W |
| `sensor.urban_energie_solaire_produite` | Énergie solaire calculée par intégration de la puissance |
| `sensor.urban_energie_consommee_totale` | Énergie consommée calculée par intégration de la puissance |
| `sensor.urban_energie_importee_enedis_raw` | Énergie importée calculée à partir de la puissance réseau |
| `sensor.urban_energie_importee_enedis` | Compteur d'énergie importée, en kWh |
| `sensor.urban_energie_restituee_au_reseau` | Bilan net production moins consommation, en kWh; peut augmenter ou diminuer |
| `sensor.urban_energie_restituee_au_reseau_hourly` | Compteur net fourni par le helper `utility_meter`, remis à zéro à chaque cycle horaire |
| `sensor.urban_batterie_virtuelle_entree_horaire` | Compteur d'énergie cumulée vers la batterie, en kWh |
| `sensor.urban_batterie_virtuelle_sortie_horaire` | Compteur d'énergie cumulée depuis la batterie, en kWh |
| `sensor.urban_batterie_virtuelle_stock_statistiques` | Copie du stock de batterie destinée aux statistiques long terme |

Les capteurs instantanés de puissance et le capteur de stock ont des statistiques de mesure. Les capteurs d'énergie utilisent des statistiques de total. Les statistiques long terme commencent à s'accumuler après l'installation; elles ne restaurent pas les états historiques déjà purgés.

### Helpers `input_number`

- `input_number.urban_energie_battery_in_hourly`
- `input_number.urban_energie_battery_out_hourly`
- `input_number.urban_batterie_virtuelle_stock`
- `input_number.urban_batterie_virtuelle_pointage`

Les helpers `urban_energie_battery_*_hourly` sont des compteurs cumulés mis à jour par l'automation horaire; ils ne représentent pas une valeur isolée remise à zéro chaque heure. Le helper `input_number.urban_batterie_virtuelle_stock` contient le stock courant. Le capteur `sensor.urban_batterie_virtuelle_stock_statistiques` en fournit une copie compatible avec les statistiques long terme.

### Automatisations incluses

- Mise à jour horaire du stock et des compteurs de batterie, à 59:45 de chaque heure.
- Le pointage manuel est appliqué puis remis à zéro par cette automation.

---

<a id="tableau-de-bord-lovelace"></a>
## 5. Tableau de bord Lovelace

Le tableau de bord montre les flux de puissance, le bilan énergétique et le stock de la batterie virtuelle. Il référence les cartes frontend listées dans la section d'installation.

Les entités `sensor.urban_batterie_virtuelle_entree_horaire` et `sensor.urban_batterie_virtuelle_sortie_horaire` peuvent servir à configurer les flux d'entrée et de sortie de batterie dans le tableau de bord Énergie. Vérifiez le sens et l'unité des compteurs avant de les sélectionner.

![Capture d'écran de l'application](https://i.imgur.com/NBjRcze.png)

![Capture d'écran de l'application](https://i.imgur.com/KdZF5rX.png)

![Capture d'écran de l'application](https://i.imgur.com/vUdDOOh.png)
---

<a id="depannage"></a>
## 6. Dépannage

- **Le formulaire refuse un capteur source ?** Vérifiez qu'il a `device_class: power` et l'unité exacte `kW`; les capteurs en `W` ne passent pas la validation actuelle.
- **Des entités UrbanSolar manquent ?** Vérifiez que l'intégration a été configurée, que les sources sélectionnées sont disponibles et que les inclusions `urban_*.yaml` sont présentes dans `configuration.yaml`. Validez la configuration et consultez les journaux Home Assistant.
- **Le stock de batterie ne se met pas à jour ?** L'automation s'exécute à `:59:45` de chaque heure. Elle ignore le cycle si `sensor.urban_energie_restituee_au_reseau_hourly` n'est pas strictement compris entre `-30` et `30` kWh.
- **Les statistiques long terme n'apparaissent pas immédiatement ?** Vérifiez que l'entité a un état numérique et un `state_class`. Les statistiques commencent après l'installation; elles ne recréent pas les états historiques déjà purgés.

### Validation HACS

La validation HACS de ce fork échoue actuellement sur trois métadonnées GitHub : aucun fichier de licence, fonctionnalité de signalement désactivée et aucun sujet reconnu. L'archive ZIP de la [publication 1.0.2](https://github.com/BeletteHome/ha-urbansolar-bv/releases/tag/v1.0.2) reste disponible pour une installation manuelle. N'ajoutez pas de licence avant d'avoir choisi celle qui s'applique à ce fork.

---

<a id="a-propos-de-ce-fork"></a>
## 7. À propos de ce fork

Ce dépôt est un fork personnel de test maintenu par BeletteHome. Il est fourni « en l'état », sans assistance ni garantie. Il n'est pas affilié au projet d'origine.

---

Merci d’utiliser cette version de test d’**UrbanSolar Battery**.
