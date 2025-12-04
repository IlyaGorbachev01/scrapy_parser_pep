BOT_NAME = 'pep_parse'

SPIDER_MODULES = ['pep_parse.spiders']
NEWSPIDER_MODULE = 'pep_parse.spiders'

ROBOTSTXT_OBEY = True

FEEDS = {
    # Файлы со списком PEP.
    'results/pep_%(time)s.csv': {
        'format': 'csv',
        'fields': ['number', 'name', 'status'],
        'overwrite': True
    },
    # Файлы со сводкой по статусам.
    'results/status_summary_%(time)s.csv': {
        'format': 'csv',
        'fields': ['status', 'count'],
        'overwrite': True
    },
}

ITEM_PIPELINES = {
    'pep_parse.pipelines.StatusSummaryPipeline': 300,
}
