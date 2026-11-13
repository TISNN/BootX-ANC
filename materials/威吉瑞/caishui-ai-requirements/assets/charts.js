// caishui-ai-requirements charts
(function() {
  var style = getComputedStyle(document.documentElement);
  var accent = style.getPropertyValue('--accent').trim();
  var accent2 = style.getPropertyValue('--accent2').trim();
  var ink = style.getPropertyValue('--ink').trim();
  var muted = style.getPropertyValue('--muted').trim();
  var rule = style.getPropertyValue('--rule').trim();
  var bg2 = style.getPropertyValue('--bg2').trim();

  /* ---- Chart 1: Pain point intensity ---- */
  var painEl = document.getElementById('chart-pain');
  if (painEl) {
    var pain = echarts.init(painEl, null, { renderer: 'svg' });
    pain.setOption({
      animation: false,
      tooltip: {
        trigger: 'axis',
        appendToBody: true,
        axisPointer: { type: 'shadow' }
      },
      grid: { left: 8, right: 40, top: 20, bottom: 8, containLabel: true },
      xAxis: {
        type: 'value', max: 10,
        axisLine: { lineStyle: { color: rule } },
        axisLabel: { color: muted },
        splitLine: { lineStyle: { color: rule } }
      },
      yAxis: {
        type: 'category', inverse: true,
        data: ['沟通效率低', '客户分层缺失', '咨询承载重', '汇报流于形式'],
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { color: ink, fontSize: 13 }
      },
      series: [{
        type: 'bar',
        data: [
          { value: 9, itemStyle: { color: accent2 } },
          { value: 8, itemStyle: { color: accent2 } },
          { value: 7, itemStyle: { color: accent } },
          { value: 5, itemStyle: { color: accent } }
        ],
        barWidth: 22,
        label: { show: true, position: 'right', color: ink, fontWeight: 700 },
        itemStyle: { borderRadius: [0, 4, 4, 0] }
      }]
    });
    window.addEventListener('resize', function() { pain.resize(); });
  }

  /* ---- Chart 2: Module phase & investment ---- */
  var prioEl = document.getElementById('chart-prio');
  if (prioEl) {
    var prio = echarts.init(prioEl, null, { renderer: 'svg' });
    prio.setOption({
      animation: false,
      tooltip: {
        trigger: 'axis',
        appendToBody: true,
        axisPointer: { type: 'shadow' }
      },
      legend: {
        data: ['一期 · 人效释放', '二期 · 咨询与获客', '三期 · 系统与自动化'],
        textStyle: { color: muted }, bottom: 0
      },
      grid: { left: 8, right: 16, top: 20, bottom: 40, containLabel: true },
      xAxis: {
        type: 'category',
        data: ['M1 沟通', 'M2 分级', 'M3 进度', 'M4 知识库', 'M5 流程', 'M6 新媒体', 'M8 数字员工', 'M7 记账重构'],
        axisLine: { lineStyle: { color: rule } },
        axisLabel: { color: muted, interval: 0, rotate: 20 }
      },
      yAxis: {
        type: 'value', name: '相对投入',
        axisLine: { lineStyle: { color: rule } },
        axisLabel: { color: muted },
        splitLine: { lineStyle: { color: rule } },
        nameTextStyle: { color: muted }
      },
      series: [
        {
          name: '一期 · 人效释放', type: 'bar', stack: 'total',
          data: [3, 3, 3, 0, 0, 0, 0, 0],
          itemStyle: { color: accent }
        },
        {
          name: '二期 · 咨询与获客', type: 'bar', stack: 'total',
          data: [0, 0, 0, 4, 3, 3, 0, 0],
          itemStyle: { color: accent2 }
        },
        {
          name: '三期 · 系统与自动化', type: 'bar', stack: 'total',
          data: [0, 0, 0, 0, 0, 0, 3, 8],
          itemStyle: { color: muted }
        }
      ]
    });
    window.addEventListener('resize', function() { prio.resize(); });
  }
})();