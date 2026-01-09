# Custom Nodes Collection for ALLPLAN VisualScripting

Welcome to this GitHub project — a **set of custom nodes** for the **ALLPLAN** VisualScripting solution.

## About the Project

This repository offers a collection of custom VisualScripting nodes designed to enhance and extend the capabilities of visual scripting in ALLPLAN. VisualScripting allows you to create parametric objects and automate processes without programming skills — simply by connecting nodes, which represent code blocks or functions, in a graphical interface.

## Features

- **Easy-to-use custom nodes**
- Seamlessly integrated into the ALLPLAN VisualScripting library

## Installation

**Custom VS Nodes From Allplan France** can be installed directly from the Plugin Manager in ALLPLAN.  
Alternatively, the corresponding .allep package can be downloaded from the [release page](https://github.com/cmaignan-source/vsnodes/releases).  
*.allep* files are ALLPLAN extension packages that can be installed via drag and drop into the program window.

## Requirements

- ALLPLAN >= 2026

## Installed Assets

The plugin installs following assets into ALLPLAN:

- VisualScripting nodes:
  - ChangeObjectAttribute
  - CommandBlock
  - GetObjectAttribute
  - IfElse
  - ListSplitByBool
  - LoopFor
  - MatchCase
  - OperatorModulo
  - SetOrCreateAttribute
  - SortObjectsByAttribute

They can be found in the Visual Editor under `Custom Library` → `STD` → `ALLPLAN FRANCE`

## Workflow

- Open the ALLPLAN VisualScripting application.
- Drag and drop the nodes from the Custom Library into your workspace.
- Configure their properties according to your needs (geometry, logic, input/output).
- Connect the nodes to create data flows or action sequences.
- Start the script: the result will be displayed in real time within the ALLPLAN view.
- Save your project as a *.avsprj* and create a *.pyp* script.

## Contributing

Contributions are welcome! You can propose new nodes, report bugs, or suggest improvements by opening an issue or a pull request.

## License

This project is distributed under the MIT License (see LICENSE.md).

## Contact

For questions, please open an issue on the repository or contact me.
