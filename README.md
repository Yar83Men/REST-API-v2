# Test_Komtek_v_2
# API with only GET HTTP method
##### Получение списка справочников
##### Метод GET url api/directory/all/

##### Получение Справочников по дате
##### url api/directory/date/?date=Y-m-d

##### Получение Элементов справочника по версии Справочника
##### url api/directory/version/?version=Версия Справочника


##### Получение элементов заданного справочника текущей версии
##### Возвращает список Элементов Справочника последней версии (последний по дате)
##### url api/directory/validate/?name=Название Справочника

##### Валидация элемента заданного справочника по указанной версии
##### Возвращает список Элементов справочника (если они есть в Справочнике) по указанной версии Справочника
##### api/directory/element/validate/?version=Версия Справочника&code=Код Элемента

##### Валидация элементов заданного справочника текущей версии
##### Возвращается список Элементов (если они есть в Справочнике) с последней датой Справочника
##### url api/directory/current/validate/?name=Название Справочника&code=Код Элемента
