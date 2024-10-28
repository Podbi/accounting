function sanitizeAmount(amount)
{
    return parseFloat(amount.replace(/,/g, ''));
}

function generateRandonColour()
{
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);

    return "rgb(" + r + "," + g + "," + b + ")";
}

function calculateChartData(tableElement)
{
    var labels = [];
    var data = [];
    var colors = [];

    $(tableElement).find('[data-table-row]').each(function(index, element) {
        labels.push($(element).find('[data-table-label]').text());
        data.push(sanitizeAmount($(element).find('[data-table-amount]').text()));
        colors.push(generateRandonColour());
    });   
    
    return {
        labels : labels,
        datasets : [{
            data : data,
            borderWidth : 1,
            backgroundColor : colors,
            borderColor: colors
        }]
    }
}

function calculateBarChartData(tableElement, label)
{
    var labels = [];
    var data = [];
    var colors = [];

    $(tableElement).find('[data-table-row]').each(function(index, element) {
        labels.push($(element).find('[data-table-label]').text());
        var amount = sanitizeAmount($(element).find('[data-table-amount]').text());
        data.push(amount);
        if (amount > 0) {
            colors.push("#dff0d8");
        } else {
            colors.push("#f2dede");
        }
    });

    return {
        labels : labels,
        datasets : [{
            label : label,
            data : data,
            borderWidth : 1,
            backgroundColor: colors
        }]
    }
}