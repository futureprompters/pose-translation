<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
<h3 align="center">PoseTranslation</h3>

  <p align="center">
    PoseTranslation is a project that enables the transfer of motion from a video onto a selected photograph. Unlike similar solutions, it allows for the direct transfer of motion from the body rather than from previously extracted poses.
    <br />
    <br />
    <a href="https://github.com/futureprompters/pose-translation/issues">Report Bug</a>
    ·
    <a href="https://github.com/futureprompters/pose-translation/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<p align="right">(<a href="#readme-top">back to top</a>)</p>


### Built With

* [![python][python.org]][python-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

* [python](https://www.python.org/)
* [docker](https://www.docker.com/)

### Installation

1. Clone the repo
    ```sh
    git clone https://github.com/futureprompters/pose-translation.git
    ```
2. Build the Docker image using the provided Dockerfile:
    ```
    docker build -t posetranslation .
    ```
3. Once the Docker image is built successfully, run the Docker container using the following command:
    ```
    docker run -p 7860:7860 posetranslation
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

The user guide will be displayed upon loading the application in Gradio.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->

<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

https://futureprompters.com or via mail - hello@xberry.tech

Project Link: [https://github.com/futureprompters/pose-translation](https://github.com/futureprompters/pose-translation)

#### check out our linkedin!


[![linkedin][linkedin-shield]][linkedin-url]


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments
* [MagicAnimate][https://showlab.github.io/magicanimate/] - huge part of this project was based on MagicAnimate
* [vid2densepose][https://github.com/Flode-Labs/vid2densepose] - The creation of this demo was made possible through the use ofvid2densepos
* [TikTokDancing][https://datasetninja.com/full-body-tiktok-dancing-dataset] - The demo utilized TikTok DancingDataset

<p align="right">(<a href="#readme-top">back to top</a>)</p>

