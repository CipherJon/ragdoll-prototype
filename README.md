# Ragdoll Prototype

A minimal physics-based ragdoll simulation using Pygame.

## Overview

This project demonstrates a simple ragdoll simulation with basic physics, including gravity, damping, and constraints. The ragdoll consists of multiple parts (head, torso, arms, legs) connected by constraints to simulate realistic movement.

## Features

- **Physics Simulation**: Gravity, damping, and constraints for realistic ragdoll behavior.
- **Interactive**: Click anywhere to reset the ragdoll to the mouse position.
- **Compact**: The entire simulation is implemented in under 200 lines of code.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ragdoll-prototype
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the simulation:
```bash
python main.py
```

- **Interact**: Click anywhere in the window to reset the ragdoll to the mouse position.

## Testing

To run the unit tests:
```bash
python -m unittest tests/test_ragdoll.py
```

## File Structure

```
ragdoll-prototype/
├── main.py               # Main simulation code
├── requirements.txt      # Dependencies
├── tests/                # Unit tests
│   └── test_ragdoll.py   # Test file for the ragdoll
├── README.md             # Project documentation
└── screenshot.png        # Screenshot of the simulation
```

## Dependencies

- `pygame`: For rendering and user interaction.
- `numpy`: Optional, for numerical operations.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

This `README.md` provides a comprehensive overview of the project, including installation instructions, usage, testing, and file structure.