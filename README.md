<div align="center">
  <img
    style="width: 165px; height: 165px"
    src="https://i.postimg.cc/y860zrtT/JA-LOGO.png"
    title="JS0Nime"
    alt="JS0Nime"
  />
  <h3>JS0Nime</h3>
  <p>
    A Python script that allows you to generate all of an anime's episodes at once.
  </p>
</div>

## About JS0Nime

**JS0Nime** is a Python script that allows you to generate links for any anime you want.
[gogoanime](https://gogoanime.pe/) provides the content for **JS0Nime**.
If you get a **404** error, please use [gogoanime](https://gogoanime.pe/) to find for the correct anime name.
You can select to acquire all of the episodes or a specific number of episodes via the script.

## Installation

```console
git clone https://github.com/sh1nobuu/JS0Nime.git
```

## Screenshot

<div align="center">
  <img style="height:386px; width:688px;" src="https://i.postimg.cc/PrWMHDxd/ja-screenshot.png"
  title="JS0Nime in action" alt="JS0Nime Screenshot">
  <img style="height:386px; width:688px;" src="https://i.postimg.cc/cLWXtmjK/generate.png" title="Shigofumi Letters from the Departed " alt="Generated anime links with JS0Nime">
</div>

## Dependencies

**JS0Nime** is highly reliant on the python modules `requests`, `colorama`, `json`, and `BeautifulSoup`.

```console
pip install -r requirements.txt
```

## Usage

The anime name is separated by "-". You can either type it manually, or go to [gogoanime.pe](https://gogoanime.pe/) and search for the anime you want to scrape and copy the name from the URL.

### Examples

##### One word title

- https://gogoanime.pe/category/bakemonogatari >> bakemonogatari
- https://gogoanime.pe/category/steinsgate >> steinsgate

##### Multiple word title

- https://gogoanime.pe/category/shadows-house >> shadows-house
- https://gogoanime.pe/category/kono-subarashii-sekai-ni-shukufuku-wo- >> kono-subarashii-sekai-ni-shukufuku-wo-
