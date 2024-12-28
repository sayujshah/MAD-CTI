# MAD-CTI: Multi-Agent Dark Web Cyber Threat Intelligence

This repository is the official code implementation for the paper _MAD-CTI: Cyber Threat Intelligence Analysis of the Dark Web Using a Multi-Agent Framework_ by Sayuj Shah and Vijay Madisetti.

## Quickstart

### Requirements

To install requirements:

```setup
pip install -r requirements.txt
```

### Replicating MAD-CTI Experiment

We have included all files used during experiment implementation. To replicate our results, you will need to request access to the [CoDA](https://huggingface.co/datasets/s2w-ai/CoDA) database. From there, set your .env variables with your OpenAI and HuggingFace API tokens. Finally, simply execute
```
python MAD_CTI_CoDA.py
```

### Using MAD-CTI With Web Scraper

To use the MAD-CTI tool with a dark web scraper, ensure [Tor](https://www.torproject.org/) is properly isntalled on your device and the SocksPort is configured as detailed in the [requests-tor documentation](https://pypi.org/project/requests-tor/). Once this is complete, set your .env variables with you OpenAI and HuggingFace API tokens, along with your torrc hashed control password and run:
```
python MAD_CTI.py
```

## Workflow Architecture

The basic architecture of the multi-agent workflow can be found below. MAD-CTI utilized [Microsoft AutoGen](https://www.microsoft.com/en-us/research/project/autogen/) to develop numerous agents the communicate with one another to complete tasks with little-to-no human intervention.
![Architecture](Docs/System Architecture.png "Architecture")

## Citing

If you make use of ThreatCrawl in your work, please cite the following paper:

```
@misc{shah2024madcti,
      title={MAD-CTI: Multi-Agent DarkWeb Cyber Threat Intelligence}, 
      author={Sayuj Shah and Vijay Madisetti},
      year={2024},
      eprint={},
      archivePrefix={},
      primaryClass={},
      url={}, 
}
```

## Contributors

- Sayuj Shah
- Vijay Madisetti

## Acknowledgements

This work was supported by the School of Cybersecurity and Privacy and the College of Computing at Georgia Institute of Technology.

## License

MIT License

Copyright (c) 2024 Sayuj Shah

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.