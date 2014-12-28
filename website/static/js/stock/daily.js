function update_table(page, psize){
    var data = {};
    data['topcat'] = $("#topcat").val();
    data['secondcat'] = $("#secondcat").val();
    data['thirdcat'] = $("#thirdcat").val();
    data['page'] = page;
    data['psize'] = psize;
    $.ajax({
	type: "get",
	data: data,
	url: "/stock/api?action=dailystock"
    }).done(function (res){
	res = $.parseJSON(res);
	if(res.code == 0){
	    var table = $("#dailydata").dataTable();
	    table.fnClearTable();
	    $.each(res.detail.data, function(i, item){
		var arr = [item.code,
			   item.name,
			   item.p_open,
			   item.p_close,
			   item.p_inc,
			   item.p_earning_ratio,
			   item.trade_money,
			   item.market_value,
			   item.is_suspend_trading]
		table.fnAddData(arr);
	    });
	    table.fnDraw();
	    console.log('success.');
	}
    });

    $.ajax({
	type: "get",
	data: data,
	url: "/stock/api?action=dailysum"
    }).done(function (res){
	res = $.parseJSON(res);
	if(res.code == 0){
	    var doughnut_data = res.detail.doughnut_data;
	    $("#chartcanvas").replaceWith('<canvas id="chartcanvas" style="width=500;height=500"></canvas>');
	    var ctx = document.getElementById("chartcanvas").getContext("2d");
	    window.myDoughnut = new Chart(ctx).Doughnut(doughnut_data, {responsive : true});
	    console.log('success.');

	    var market_value_data = res.detail.market_value_data;
	    $("#canvas").replaceWith('<canvas  id="canvas" style="width=300;height=100"></canvas>');
	    var ctx = document.getElementById("canvas").getContext("2d");
	    window.myBar = new Chart(ctx).Bar(market_value_data, {responsive : true});
	}
    });
}

$("#topcat").change(function(){
    var catid = $(this).val();
    $.ajax({
	type: "get",
	url: "/stock/api?action=childcat&catid=" + catid
    }).done(function (data){
	data = $.parseJSON(data);
	if(data.code==0){
	    if(data.detail.cats.length > 0){
		$('#secondcat').empty().append('<option value="-1" selected="selected">--</option>')
		$.each(data.detail.cats, function(i, cat){
		    $('#secondcat').append('<option value="' + cat.id + '">'+ cat.name + '</option>')
		});
	    }else{
		$('#secondcat').empty().append('<option value="-1" selected="selected">--</option>')
		$('#thirdcat').empty().append('<option value="-1" selected="selected">--</option>')
		update_table(1, 100);
	    }
	}
    });
})

$("#secondcat").change(function(){
    var catid = $(this).val();
    $.ajax({
	type: "get",
	url: "/stock/api?action=childcat&catid=" + catid
    }).done(function (data){
	data = $.parseJSON(data);
	if(data.code==0){
	    if(data.detail.cats.length > 0){
		$('#thirdcat').empty().append('<option value="-1" selected="selected">--</option>');
		$.each(data.detail.cats, function(i, cat){
		    $('#thirdcat').append('<option value="' + cat.id + '">'+ cat.name + '</option>')
		});
	    }else{
		$('#thirdcat').empty().append('<option value="-1" selected="selected">--</option>');
		update_table(1, 100);
	    }
	}
    });
})

$(".btn-default").click(function(){
    update_table(1, 100);
})

