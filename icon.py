import json
import os
import warnings

from PyQt5.QtCore import QObject, QPoint, QRect, Qt
from PyQt5.QtGui import (QColor, QFont, QFontDatabase, QIcon, QIconEngine,
                        QPainter, QPixmap)
from PyQt5.QtWidgets import QApplication


SYSTEM_FONTS = False


class CharIconPainter:

    """Char icon painter."""

    def paint(self, iconic, painter, rect, mode, state, options):
        """Main paint method."""
        for opt in options:
            self._paint_icon(iconic, painter, rect, mode, state, opt)

    def _paint_icon(self, iconic, painter, rect, mode, state, options):
        """Paint a single icon."""
        painter.save()
        color = options['color']
        char = options['char']

        color_options = {
            QIcon.On: {
                QIcon.Normal: (options['color_on'], options['on']),
                QIcon.Disabled: (options['color_on_disabled'],
                                 options['on_disabled']),
                QIcon.Active: (options['color_on_active'],
                               options['on_active']),
                QIcon.Selected: (options['color_on_selected'],
                                 options['on_selected'])
            },

            QIcon.Off: {
                QIcon.Normal: (options['color_off'], options['off']),
                QIcon.Disabled: (options['color_off_disabled'],
                                 options['off_disabled']),
                QIcon.Active: (options['color_off_active'],
                               options['off_active']),
                QIcon.Selected: (options['color_off_selected'],
                                 options['off_selected'])
            }
        }

        color, char = color_options[state][mode]

        painter.setPen(QColor(color))

        # A 16 pixel-high icon yields a font size of 14, which is pixel perfect
        # for font-awesome. 16 * 0.875 = 14
        # The reason why the glyph size is smaller than the icon size is to
        # account for font bearing.

        draw_size = 0.875 * round(rect.height() * options['scale_factor'])
        prefix = options['prefix']

        # Animation setup hook
        animation = options.get('animation')
        if animation is not None:
            animation.setup(self, painter, rect)
        font = QFont('Material Design Icons')
        font.setPixelSize(draw_size)
        painter.setFont(font)
        if 'offset' in options:
            rect = QRect(rect)
            rect.translate(options['offset'][0] * rect.width(),
                           options['offset'][1] * rect.height())

        painter.setOpacity(options.get('opacity', 1.0))

        painter.drawText(rect, Qt.AlignCenter | Qt.AlignVCenter, char)
        painter.restore()


class FontError(Exception):
    """Exception for font errors."""


class CharIconEngine(QIconEngine):

    """Specialization of QIconEngine used to draw font-based icons."""

    def __init__(self, iconic, painter, options):
        super(CharIconEngine, self).__init__()
        self.iconic = iconic
        self.painter = painter
        self.options = options

    def paint(self, painter, rect, mode, state):
        self.painter.paint(
            self.iconic, painter, rect, mode, state, self.options)

    def pixmap(self, size, mode, state):
        pm = QPixmap(size)
        pm.fill(Qt.transparent)
        self.paint(QPainter(pm), QRect(QPoint(0, 0), size), mode, state)
        return pm


class IconicFont(QObject):

    """Main class for managing iconic fonts."""

    def __init__(self):
        super(IconicFont, self).__init__()
        self.painter = CharIconPainter()
        self.painters = {}
        self.fontname = {}
        self.charmap = {}
        self.load_font()

    def load_font(self):
        directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
        charmap_filename = 'materialdesignicons-webfont-charmap.json'

        def hook(obj):
            result = {}
            for key in obj:
                result[key] = chr(int(obj[key], 16))
            return result

        with open(os.path.join(directory, charmap_filename), 'r') as codes:
            self.charmap['mdi'] = json.load(codes, object_hook=hook)

    def icon(self, *names, **kwargs):
        """Return a QIcon object corresponding to the provided icon name."""
        options_list = kwargs.pop('options', [{}] * len(names))
        general_options = kwargs

        if len(options_list) != len(names):
            error = '"options" must be a list of size {0}'.format(len(names))
            raise Exception(error)

        if QApplication.instance() is not None:
            if self.fontname.get('mdi') is None:
                directory = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'fonts')
                ttf_filename = 'materialdesignicons-webfont.ttf'
                id_ = QFontDatabase.addApplicationFont(os.path.join(directory, ttf_filename))
                loadedFontFamilies = QFontDatabase.applicationFontFamilies(id_)
                if(loadedFontFamilies):
                    self.fontname['mdi'] = loadedFontFamilies[0]

            parsed_options = []
            for i in range(len(options_list)):
                specific_options = options_list[i]
                parsed_options.append(self._parse_options(specific_options,
                                                          general_options,
                                                          names[i]))
            engine = CharIconEngine(self, self.painter, parsed_options)
            return QIcon(engine)
        else:
            warnings.warn("You need to have a running "
                          "QApplication to use QtAwesome!")
            return QIcon()

    def _parse_options(self, specific_options, general_options, name):
        _default_options = {
            'color': QColor(50, 50, 50),
            'color_disabled': QColor(150, 150, 150),
            'opacity': 1.0,
            'scale_factor': 1.0,
        }
        options = dict(_default_options, **general_options)
        options.update(specific_options)
        icon_kw = ['char', 'on', 'off', 'active', 'selected', 'disabled',
                   'on_active', 'on_selected', 'on_disabled', 'off_active',
                   'off_selected', 'off_disabled']
        char = options.get('char', name)
        on = options.get('on', char)
        off = options.get('off', char)
        active = options.get('active', on)
        selected = options.get('selected', active)
        disabled = options.get('disabled', char)
        on_active = options.get('on_active', active)
        on_selected = options.get('on_selected', selected)
        on_disabled = options.get('on_disabled', disabled)
        off_active = options.get('off_active', active)
        off_selected = options.get('off_selected', selected)
        off_disabled = options.get('off_disabled', disabled)

        icon_dict = {'char': char,
                     'on': on,
                     'off': off,
                     'active': active,
                     'selected': selected,
                     'disabled': disabled,
                     'on_active': on_active,
                     'on_selected': on_selected,
                     'on_disabled': on_disabled,
                     'off_active': off_active,
                     'off_selected': off_selected,
                     'off_disabled': off_disabled,
                     }
        names = [icon_dict.get(kw, name) for kw in icon_kw]
        chars = self._get_prefix_chars(names)
        options.update(dict(zip(*(icon_kw, chars))))
        options.update({'prefix': 'mdi'})

        # Handle colors for modes (Active, Disabled, Selected, Normal)
        # and states (On, Off)
        color = options.get('color')
        options.setdefault('color_on', color)
        options.setdefault('color_active', options['color_on'])
        options.setdefault('color_selected', options['color_active'])
        options.setdefault('color_on_active', options['color_active'])
        options.setdefault('color_on_selected', options['color_selected'])
        options.setdefault('color_on_disabled', options['color_disabled'])
        options.setdefault('color_off', color)
        options.setdefault('color_off_active', options['color_active'])
        options.setdefault('color_off_selected', options['color_selected'])
        options.setdefault('color_off_disabled', options['color_disabled'])
        return options

    def _get_prefix_chars(self, names):
        chars = []
        for name in names:
            chars.append(self.charmap['mdi'][name])
        return chars


icon_font = IconicFont()
