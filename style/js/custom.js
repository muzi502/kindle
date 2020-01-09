$(function(){

	//嵌入笔记
	$('.panel-body').each(function(){
		var hi = $(this).attr('class'),
			mk = new RegExp(/\d+$/),
			m = mk.exec(hi),
			nt = $('.nt'+m).html();
		if( $(this).hasClass('mk'+m) && nt != null ){
			$('.nt'+m).parents('article').hide();
			$(this).append(
				'<div class="well well-sm"> \
					<span class="label label-default">笔记</span> \
					<div class="noteCont">' + nt +'</div> \
				</div>'
			);
		}
	});

	//侧边浮动
	$.fn.smartFloat = function() {
		//定义定位参数
		var position = function(element) {
			var phd = $('.header').height() - 20,
				top = element.position().top + phd,
				pos = element.css("position");
			//实时监测
			$(window).on('resize scroll', function() {
				var scrolls = $(this).scrollTop(),
					ep = element.parent().width(); //浮动元素宽度跟随其父元素宽度变动
				//当页面顶部超过 top 定义的高度 && 窗口宽度大于 991
				if (scrolls > top && $(window).width() > 991 ) {
					if (window.XMLHttpRequest) {
						element.css({
							position: "fixed",
							top: '20px',
							width: ep
						});
					} else {
						element.css({
							top: scrolls,
							width: 'auto'
						});
					}
				//否则就复原
				}else {
					element.css({
						position: pos,
						top: top,
						width: 'auto'
					});
				}
			});
		};
		//返回定位参数
		return $(this).each(function() {
			position($(this));
		});
	};
	//绑定
	$(".nav-pills").smartFloat();

});