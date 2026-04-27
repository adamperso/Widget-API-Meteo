# 🤖 OpenJarvis

**Your Personal AI Agent - Autonomous Coding Assistant**

OpenJarvis est un agent IA personnel puissant capable de coder, tester, corriger et automatiser des tâches. Inspiré par GitHub Copilot et Codex, mais entièrement contrôlable et exécutable en local.

## 🏗️ Architecture

```
OpenJarvis/
├── jarvis/                    # Cœur de l'agent
│   ├── agent/                 # Boucle principale, planification, mémoire
│   ├── tools/                 # Outils (fichiers, shell, recherche)
│   ├── llm/                   # Connexion aux modèles (Ollama, OpenAI)
│   └── utils/                 # Utilitaires
├── config/                    # Configuration
├── memory/                    # Mémoire persistante
├── bot.js                     # Bridge WhatsApp
└── scripts/                   # Scripts d'installation
```

## ✨ Fonctionnalités

### V1 (Actuel)
- ✅ CLI Jarvis (`uv run jarvis ask`)
- ✅ Agent autonome avec boucle de réflexion
- ✅ Exécution de commandes shell
- ✅ Modification de fichiers
- ✅ Lecture de code
- ✅ Réponse intelligente

### 🔥 Fonctionnalités Avancées (Évolutives)
- 🤖 Agent développeur (corrige bugs, génère code, refactor)
- 🔁 Auto-correction (lance tests, corrige erreurs, retry)
- 🧠 Planification (décompose tâches complexes)
- 💬 Multi-interface (CLI, WhatsApp, Web UI à venir)
- 🧠 Mémoire persistante (se souvient du projet)
- 🔐 Sécurité (whitelist commandes, confirmation actions)

## 🚀 Installation

### Prérequis

- **Python 3.10+**
- **Node.js 18+**
- **Git**

### 1. Cloner le projet

```bash
git clone <repository-url>
cd OpenJarvis
```

### 2. Lancer le script d'installation

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### 3. Configuration

#### Option A: Ollama (Local - Recommandé)

```bash
# Installer Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Télécharger un modèle
ollama pull deepseek-coder

# Démarrer Ollama
ollama serve
```

#### Option B: OpenAI (Cloud)

Éditez `.env` et ajoutez votre clé API:

```bash
OPENAI_API_KEY=sk-...
MODEL=gpt-4
```

## 📖 Utilisation

### CLI - Commande de base

```bash
# Poser une question
uv run jarvis ask "Crée un fichier Python qui affiche Hello World"

# Demander une tâche complexe
uv run jarvis ask "Refactorise ce code pour utiliser des classes"

# Lister des fichiers
uv run jarvis ask "Liste tous les fichiers .py dans le projet"
```

### WhatsApp Bot

```bash
# Démarrer le bot
npm start

# Scanner le QR code avec WhatsApp
# Envoyer un message: "jarvis crée un fichier test.py"
```

### Exemples de commandes

```bash
# Création de code
uv run jarvis ask "Crée une API REST avec Flask"

# Debugging
uv run jarvis ask "Trouve et corrige les bugs dans main.py"

# Recherche
uv run jarvis ask "Cherche toutes les fonctions qui utilisent requests"

# Automatisation
uv run jarvis ask "Crée un script qui backup mes fichiers"
```

## 🧠 Composants Principaux

### 1. Agent Loop (`jarvis/agent/loop.py`)

Cœur du système. Il:
- Envoie le prompt au LLM
- Analyse la réponse
- Détecte les appels d'outils
- Exécute les outils
- Retourne le résultat au LLM
- Boucle jusqu'à la réponse finale

### 2. Tools (`jarvis/tools/`)

| Outil | Description |
|-------|-------------|
| `read_file` | Lire un fichier |
| `write_file` | Écrire/créer un fichier |
| `list_directory` | Lister un dossier |
| `run_command` | Exécuter commande shell |
| `run_python` | Exécuter code Python |
| `grep` | Chercher dans le code |
| `find_files` | Trouver des fichiers |

### 3. LLM (`jarvis/llm/`)

Supporte plusieurs providers:
- **Ollama** (local): deepseek-coder, qwen, llama2
- **OpenAI** (cloud): gpt-4, gpt-3.5-turbo

### 4. Planner (`jarvis/agent/planner.py`)

Décompose les tâches complexes:
```
"Créer une API"
→ Planifier → Coder → Tester → Corriger
```

### 5. Memory (`jarvis/agent/memory.py`)

- Historique des actions
- Contexte long terme
- Apprentissage du projet

## ⚙️ Configuration

### `config/settings.yaml`

```yaml
llm:
  provider: ollama
  model: deepseek-coder
  
agent:
  max_iterations: 10
  auto_confirm: false

security:
  allowed_commands:
    - ls
    - cat
    - python3
```

### `.env`

```bash
# Ollama
OLLAMA_HOST=http://localhost:11434
MODEL=deepseek-coder

# Ou OpenAI
# OPENAI_API_KEY=your-key
# MODEL=gpt-4
```

## 🔐 Sécurité

L'agent inclut des protections:

- **Whitelist de commandes**: Seules certaines commandes sont autorisées
- **Confirmation requise**: Pour les actions sensibles (delete, run_command)
- **Timeout**: Limite de temps pour les exécutions
- **Logs**: Toutes les actions sont journalisées

## 📊 Logs

Les logs sont sauvegardés dans `logs/`:

```bash
tail -f logs/jarvis_*.log
```

## 🛠️ Développement

### Structure des modules

```python
# Exemple: Créer un nouvel outil
from jarvis.tools.registry import ToolRegistry

registry = ToolRegistry()
registry.register_tool(
    name="my_tool",
    func=my_function,
    description="What it does",
    parameters={"param": {"type": "string"}}
)
```

### Tests

```bash
# Lancer les tests
pytest tests/

# Formatage
black jarvis/

# Linting
flake8 jarvis/
```

## 🤝 Contribuer

1. Fork le projet
2. Crée une branche (`git checkout -b feature/amazing-feature`)
3. Commit (`git commit -m 'Add amazing feature'`)
4. Push (`git push origin feature/amazing-feature`)
5. Pull Request

## 📝 License

MIT License - voir [LICENSE](LICENSE)

## 🙏 Remerciements

- [Ollama](https://ollama.ai) - Modèles locaux
- [OpenAI](https://openai.com) - API GPT
- [whatsapp-web.js](https://github.com/pedroslopez/whatsapp-web.js) - Bridge WhatsApp

## 📞 Support

- Issues: [GitHub Issues](issues)
- Discussion: [Discussions](discussions)

---

**🚀 Construit avec ❤️ pour l'automatisation intelligente**
