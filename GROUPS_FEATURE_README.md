# Группы в ArchiMate MCP Server

## Обзор

Сервер ArchiMate MCP теперь поддерживает **именованные группы** (named groups) и **вложенные группы** (nested groups), что позволяет создавать логические контейнеры для элементов диаграммы, аналогично PlantUML группирующим конструкциям.

## Поддерживаемые типы групп

- `package` - Пакет
- `node` - Узел
- `folder` - Папка
- `frame` - Рамка
- `cloud` - Облако
- `database` - База данных
- `rectangle` - Прямоугольник

## API Структура

### Группа (GroupInput)

```json
{
  "id": "unique_group_id",
  "name": "Display Name",
  "group_type": "package|node|folder|frame|cloud|database|rectangle",
  "parent_group_id": "optional_parent_group_id",
  "description": "Optional description",
  "properties": {}
}
```

### Элемент с группой (ElementInput)

```json
{
  "id": "element_id",
  "name": "Element Name",
  "element_type": "Application_Component",
  "layer": "Application",
  "group_id": "group_id_to_assign_to"
}
```

### Диаграмма с группами (DiagramInput)

```json
{
  "title": "Diagram Title",
  "groups": [
    {
      "id": "web_group",
      "name": "Web Components",
      "group_type": "package"
    },
    {
      "id": "db_group",
      "name": "Database",
      "group_type": "database"
    },
    {
      "id": "nested_folder",
      "name": "Data Folder",
      "group_type": "folder",
      "parent_group_id": "db_group"
    }
  ],
  "elements": [
    {
      "id": "web_server",
      "name": "Web Server",
      "element_type": "Application_Component",
      "layer": "Application",
      "group_id": "web_group"
    },
    {
      "id": "database",
      "name": "MySQL",
      "element_type": "Technology_Artifact",
      "layer": "Technology",
      "group_id": "db_group"
    }
  ],
  "relationships": [...],
  "layout": {
    "group_by_groups": true
  }
}
```

## Пример использования

Пример, эквивалентный вашему PlantUML коду:

```json
{
  "title": "Grouped Architecture",
  "groups": [
    {
      "id": "web_group",
      "name": "Some Group",
      "group_type": "package"
    },
    {
      "id": "infra_group",
      "name": "Other Groups",
      "group_type": "node"
    },
    {
      "id": "cloud_group",
      "name": "Cloud Environment",
      "group_type": "cloud"
    },
    {
      "id": "mysql_db",
      "name": "MySql",
      "group_type": "database"
    },
    {
      "id": "data_folder",
      "name": "This is my folder",
      "group_type": "folder",
      "parent_group_id": "mysql_db"
    },
    {
      "id": "config_frame",
      "name": "Foo",
      "group_type": "frame",
      "parent_group_id": "mysql_db"
    }
  ],
  "elements": [
    {
      "id": "http",
      "name": "HTTP",
      "element_type": "Application_Component",
      "layer": "Application"
    },
    {
      "id": "first_comp",
      "name": "First Component",
      "element_type": "Application_Component",
      "layer": "Application",
      "group_id": "web_group"
    },
    {
      "id": "another_comp",
      "name": "Another Component",
      "element_type": "Application_Component",
      "layer": "Application",
      "group_id": "web_group"
    },
    {
      "id": "ftp",
      "name": "FTP",
      "element_type": "Application_Component",
      "layer": "Application"
    },
    {
      "id": "second_comp",
      "name": "Second Component",
      "element_type": "Application_Component",
      "layer": "Application",
      "group_id": "infra_group"
    },
    {
      "id": "example1",
      "name": "Example 1",
      "element_type": "Application_Component",
      "layer": "Application",
      "group_id": "cloud_group"
    },
    {
      "id": "folder3",
      "name": "Folder 3",
      "element_type": "Application_Component",
      "layer": "Application",
      "group_id": "data_folder"
    },
    {
      "id": "frame4",
      "name": "Frame 4",
      "element_type": "Application_Component",
      "layer": "Application",
      "group_id": "config_frame"
    }
  ],
  "relationships": [
    {
      "id": "rel1",
      "from_element": "another_comp",
      "to_element": "example1",
      "relationship_type": "Association"
    },
    {
      "id": "rel2",
      "from_element": "example1",
      "to_element": "folder3",
      "relationship_type": "Association"
    }
  ],
  "layout": {
    "group_by_groups": true
  }
}
```

## Генерируемый PlantUML код

```plantuml
@startuml
' ... styling ...

package "Some Group" {
  Application_Component(first_comp, "First Component")
  Application_Component(another_comp, "Another Component")
}

node "Other Groups" {
  Application_Component(second_comp, "Second Component")
}

cloud "Cloud Environment" {
  Application_Component(example1, "Example 1")
}

database "MySql" {
  folder "This is my folder" {
    Application_Component(folder3, "Folder 3")
  }
  frame "Foo" {
    Application_Component(frame4, "Frame 4")
  }
}

Application_Component(http, "HTTP")
Application_Component(ftp, "FTP")

' Relationships
Rel_Association(another_comp, example1, "association")
Rel_Association(example1, folder3, "association")

@enduml
```

## Важные замечания

1. **Автоматическое включение**: Если в диаграмме есть группы, `group_by_groups` автоматически устанавливается в `true`
2. **Валидация**: Сервер проверяет корректность ссылок между элементами, группами и родительскими группами
3. **Иерархия**: Группы могут быть вложенными произвольной глубины
4. **Без групп**: Элементы без `group_id` размещаются вне групп

## Совместимость

Новая функциональность полностью обратно совместима. Существующие диаграммы без групп продолжают работать как прежде.