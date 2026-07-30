# Task 2. Динамическое масштабирование контейнеров

## Предварительные шаги
Установите Locust для генерации нагрузки:
```bash
pip install locust
```

Установите Minikube и запустите кластер:
```bash
minikube start --driver=docker --container-runtime=docker --cpus=4 --memory=7835
```

Скачайте образ для платформы AMD64Скачайте образ для платформы AMD64
```bash
docker pull --platform linux/amd64 ghcr.io/yandex-practicum/scaletestapp:latest
```

Загрузите скачанный образ в MinikubeЗагрузите скачанный образ в Minikube
```bash
minikube image load ghcr.io/yandex-practicum/scaletestapp:latest
```

Проверить:

```bash
minikube status
kubectl get nodes
```

Ожидается узел со статусом `Ready`.

Активируйте metrics-server (необходим для HPA):
```bash
minikube addons enable metrics-server
```

Убедитесь, что metrics-server работает:
```bash
kubectl get pods -n kube-system | grep metrics-server
```

Проверьте метрики:

```bash
kubectl top nodes
```

## Применение манифестов
Выполните команды:

```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl apply -f hpa.yaml
```

Проверьте состояние:
```bash
kubectl get deployments
```

```bash
kubectl get pods
```

```bash
kubectl get hpa
```

![Проверка состояния после применения манифестов.png](%D0%9F%D1%80%D0%BE%D0%B2%D0%B5%D1%80%D0%BA%D0%B0%20%D1%81%D0%BE%D1%81%D1%82%D0%BE%D1%8F%D0%BD%D0%B8%D1%8F%20%D0%BF%D0%BE%D1%81%D0%BB%D0%B5%20%D0%BF%D1%80%D0%B8%D0%BC%D0%B5%D0%BD%D0%B5%D0%BD%D0%B8%D1%8F%20%D0%BC%D0%B0%D0%BD%D0%B8%D1%84%D0%B5%D1%81%D1%82%D0%BE%D0%B2.png)

Получите URL для доступа к сервису:
```bash
minikube service scaletestapp-svc --url
```

Окно Terminal, в котором она работает, нужно оставить открытым.

Команда выводит URL, например `http://127.0.0.1:57041`. Скопируйте его. В другом окне Terminal задайте переменную вручную:

```bash
export SERVICE_URL="http://127.0.0.1:57041"
```

Проверка приложения:

```bash
curl "$SERVICE_URL/"
```

Ответ должен содержать идентификатор pod.

Проверка Prometheus-метрик приложения:

```bash
curl "$SERVICE_URL/metrics"
```

В ответе должна присутствовать метрика `http_requests_total`.

## Генерация нагрузки с помощью Locust

Запустите Locust:

```bash
locust
```

Откройте браузер по адресу http://localhost:8089. 

Установите:
- Number of users (пиковая нагрузка) – например, 500.
- Spawn rate – 50 пользователей в секунду.
- Хост – укажите URL сервиса.
- Запустите тест и наблюдайте за поведением HPA:

```bash
# В другом терминале следите за HPA
kubectl get hpa -w
``````
Или откройте дашборд Minikube:

```bash
minikube dashboard
```
В разделе Deployments вы увидите, как количество реплик растёт при росте потребления памяти. Метрика http_requests_total (доступна по /metrics) также покажет рост числа запросов.