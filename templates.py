import os
import pandas as pd
from django.template import Template, Context
from django.template.engine import Engine
from django.conf import settings

settings.configure(DEBUG=False)
engine = Engine(dirs=[os.path.join(os.getcwd(), 'templates')])


def save_static_html(filename, base_template, context_dict):
    template = Template(open(f"templates/{base_template}").read(), engine=engine)
    output = template.render(
        Context(context_dict)
    )
    with open(filename, 'w') as static_html_file:
        static_html_file.write(output)


def sobre_mi():
    context = {
        'title': 'Sobre mí',
        'active': {'sobre_mi': True},
        'images': pd.read_csv('data/photos/estallido.csv').to_dict(orient='records')
    }
    save_static_html('index.html', 'sobre_mi.html', context)


def gallery(photos_csv_path, title, filename):
    images_df = pd.read_csv(photos_csv_path)
    images_df['date'] = pd.to_datetime(images_df['date'], format="%d/%m/%Y")
    images_df['date_str'] = images_df['date'].dt.strftime("%d/%m/%Y")
    images = images_df.sort_values(by='date').to_dict(orient='records')
    context = {
        'title': title,
        'active': {'fotos': True},
        'images': images
    }
    save_static_html(filename, 'galeria.html', context)


def estallido_social():
    gallery('data/photos/estallido.csv', 'Estado de excepción (Santiago de Chile, 2019)', 'estallido.html')


if __name__ == '__main__':
    sobre_mi()
    estallido_social()


# git reset --hard
# git pull