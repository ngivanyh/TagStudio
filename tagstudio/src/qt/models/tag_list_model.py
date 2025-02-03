# Copyright (C) 2025 Travis Abendshien (CyanVoxel).
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio


import typing

import src.qt.modals.build_tag as build_tag
import structlog
from PySide6.QtCore import QAbstractListModel, QSize, Qt, Signal
from PySide6.QtGui import QColor, QShowEvent
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QListView,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)
from src.core.constants import RESERVED_TAG_END, RESERVED_TAG_START
from src.core.library import Library, Tag
from src.core.library.alchemy.enums import TagColorEnum
from src.core.palette import ColorType, get_tag_color
from src.qt.translations import Translations
from src.qt.widgets.panel import PanelModal, PanelWidget
from src.qt.widgets.tag import (
    TagWidget,
    get_border_color,
    get_highlight_color,
    get_primary_color,
    get_text_color,
)

logger = structlog.get_logger(__name__)


class TagListModel(QAbstractListModel):
    def __init__(self, tags=None) -> None:
        super().__init__()
        self.tags = tags or []

    def data(self, index, role):
        tag: Tag = self.tags[index.row()]

        primary_color = get_primary_color(tag)
        border_color = (
            get_border_color(primary_color)
            if not (tag.color and tag.color.secondary)
            else (QColor(tag.color.secondary))
        )
        highlight_color = get_highlight_color(
            primary_color
            if not (tag.color and tag.color.secondary)
            else QColor(tag.color.secondary)
        )
        text_color: QColor
        if tag.color and tag.color.secondary:
            text_color = QColor(tag.color.secondary)
        else:
            text_color = get_text_color(primary_color, highlight_color)

        if role == Qt.DisplayRole:
            return tag.name

        if role == Qt.BackgroundRole:
            return primary_color

        if role == Qt.ForegroundRole:
            return text_color
        # if role == Qt.DecorationRole:
        #     tag: Tag = self.tags[index.row()]
        #     return QColor(tag.color_slug)

    def rowCount(self, index):
        return len(self.tags)
