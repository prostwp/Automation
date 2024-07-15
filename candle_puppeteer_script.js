const puppeteer = require('puppeteer-core');
const winston = require('winston');

// Конфигурация логирования
const logger = winston.createLogger({
    level: 'info',
    format: winston.format.combine(
        winston.format.timestamp({
            format: 'YYYY-MM-DD HH:mm:ss'
        }),
        winston.format.printf(({ timestamp, level, message }) => {
            return `${timestamp} [${level.toUpperCase()}]: ${message}`;
        })
    ),
    transports: [
        new winston.transports.File({ filename: 'log.txt' })
    ]
});

// Добавим логирование начала выполнения скрипта
logger.info('Начало выполнения скрипта');

try {
    // Получаем аргументы командной строки
    const args = process.argv.slice(2);

    const direction = args[0];
    const timeframe = args[1];
    const dataState = args[2];
    const pattern = args[3];
    const supResFlag = args[4] === '1';

    (async () => {
        try {
            // Чтение валютной пары из аргумента dataState
            const currencyPair = dataState;
            let titleText;

            if (pattern === "Triangle") {
                titleText = "{{ 'space_figures_title_formed_pattern' | trans ({ '[symbol]': symbol, '[pattern]': 'Triangle' }) | raw }}";
            } else {
                // Создание строки для вставки в поле #title
                titleText = direction === 'buy' ?
                    `{{ 'space_figures_title_formed_bullbear_pattern' | trans ({ '[symbol]': symbol, '[bullish_bearish]': 'space_trend_bullish' | trans, '[pattern]': '${pattern}' }) | raw }}` :
                    `{{ 'space_figures_title_formed_bullbear_pattern' | trans ({ '[symbol]': symbol, '[bullish_bearish]': 'space_trend_bearish' | trans, '[pattern]': '${pattern}' }) | raw }}`;
            }

            console.log(titleText);
            const browserURL = 'http://127.0.0.1:9222';  // Порт для подключения к Chrome
            const browser = await puppeteer.connect({ browserURL, defaultViewport: null });
            const targetUrl = 'https://cp.octafeed.com/panel/overview-posts/create';  // URL целевой страницы
            const pages = await browser.pages();

            // Найти последнюю вкладку с нужным URL
            let page = null;
            for (let i = pages.length - 1; i >= 0; i--) {
                if (pages[i].url().includes(targetUrl)) {
                    page = pages[i];
                    break;
                }
            }

            if (!page) {
                logger.error('Не удалось найти вкладку с нужным URL.');
                await browser.disconnect();
                return;
            }

            logger.info(`Используем страницу с URL: ${page.url()}`);
            logger.info(`Всего открытых страниц: ${pages.length}`);

            // Ожидание загрузки элемента ввода title
            await page.waitForSelector('#title');
            logger.info('Элемент ввода title найден');

            // Вставка текста в элемент с id="title"
            await page.type('#title', titleText);
            logger.info(`Введен текст "${titleText}" в поле title`);

            // Пауза на 1 секунду
            await new Promise(resolve => setTimeout(resolve, 200));

            // Ожидание загрузки элемента ввода channel
            await page.waitForSelector('#channel');
        logger.info('Элемент ввода channel найден');

        // Вставка валютной пары и текста "candle" в элемент с id="channel" и нажатие Enter
        await page.type('#channel', `${currencyPair.trim()} candle`);
        await page.keyboard.press('Enter');
        logger.info(`Введен текст "${currencyPair.trim()} candle" и нажата клавиша Enter в поле channel`);

        // Пауза на 0.2 секунды
        await new Promise(resolve => setTimeout(resolve, 200));

        // Ожидание загрузки элемента ввода educationPost
        await page.waitForSelector('#educationPost');
        logger.info('Элемент ввода educationPost найден');

        // Вставка текста "pattern" в элемент с id="educationPost" и нажатие Enter
        await page.type('#educationPost', pattern);
        await page.keyboard.press('Enter');
        logger.info('Введен текст "pattern" и нажата клавиша Enter в поле educationPost');

        // Пауза на 1 секунду
        await new Promise(resolve => setTimeout(resolve, 200));

        // Ожидание загрузки второго элемента ant-select-selector
        await page.waitForSelector('.ant-select-selection-search input');
        const antSelectInputs = await page.$$('.ant-select-selection-search input');

        // Проверка количества найденных элементов
        logger.info(`Найдено элементов ant-select-selection-search input: ${antSelectInputs.length}`);

        if (antSelectInputs.length < 2) {
            throw new Error('Второй элемент ant-select-selector не найден');
        }

        logger.info('Второй элемент ant-select-selector найден');
        if (supResFlag) {
            await antSelectInputs[3].type("support");
            await page.keyboard.press('Enter');
            logger.info('Введен текст "support" и нажата клавиша Enter во второй ant-select-selector');
        }
        await new Promise(resolve => setTimeout(resolve, 100));

        // Вставка текста "support" во второй ant-select-selector и нажатие Enter
        await antSelectInputs[3].type("candle");
        await page.keyboard.press('Enter');
        logger.info('Введен текст "support" и нажата клавиша Enter во второй ant-select-selector');
            // Пауза на 1 секунду
            await new Promise(resolve => setTimeout(resolve, 200));

            // Ожидание загрузки элемента ввода dealsAttribution_timeframe
            await page.waitForSelector('#dealsAttribution_timeframe');
            logger.info('Элемент ввода dealsAttribution_timeframe найден');

            // Вставка значения timeframe в элемент с id="dealsAttribution_timeframe"
            const timeframeInput = await page.$('#dealsAttribution_timeframe');
            await timeframeInput.click();
            let arrowDownPresses;
            switch (timeframe) {
                case '1.0':
                    arrowDownPresses = 0;
                    break;
                case '5.0':
                    arrowDownPresses = 1;
                    break;
                case '15.0':
                    arrowDownPresses = 2;
                    break;
                case '30.0':
                    arrowDownPresses = 3;
                    break;
                case '60.0':
                    arrowDownPresses = 4;
                    break;
                default:
                    arrowDownPresses = 0;
                    break;
            }
            for (let i = 0; i < arrowDownPresses; i++) {
                await page.keyboard.press('ArrowDown');
                await new Promise(resolve => setTimeout(resolve, 200)); // Пауза между нажатиями
            }
            await page.keyboard.press('Enter');
            logger.info(`Выбран элемент "${timeframe}" в dealsAttribution_timeframe`);

            // Пауза на 1 секунду
            await new Promise(resolve => setTimeout(resolve, 200));

            // Ожидание загрузки элементов checkbox
            await page.waitForSelector('.ant-checkbox-input');
            logger.info('Элементы ввода checkbox найдены');

            // Клик по второму checkbox
            await page.evaluate(() => {
                document.querySelectorAll('.ant-checkbox-input')[1].click();
            });
            logger.info('Клик по второму checkbox');

            // Пауза на 1 секунду
            await new Promise(resolve => setTimeout(resolve, 200));

            // Ожидание загрузки элемента ввода tradingCondition_direction
            await page.waitForSelector('#tradingCondition_direction');
            logger.info('Элемент ввода tradingCondition_direction найден');

            // Вставка значения direction в элемент с id="tradingCondition_direction"
            await page.type('#tradingCondition_direction', direction);
            if (direction === "sell") {
                await page.keyboard.press('ArrowDown');
            }
            await page.keyboard.press('Enter');
            logger.info(`Введено значение "${direction}" в поле tradingCondition_direction`);

            // Пауза на 1 секунду
            await new Promise(resolve => setTimeout(resolve, 1000));

            // Отключение без закрытия браузера
            await browser.disconnect();
            logger.info('Скрипт Puppeteer завершен');
        } catch (error) {
            logger.error(`Ошибка при выполнении скрипта Puppeteer: ${error.message}`);
        }
    })();
} catch (error) {
    logger.error(`Ошибка: ${error.message}`);
}
