function sanitizeAmount(amount)
{
    amount = parseFloat(amount.replace(/,/g, ''));

    return isNaN(amount) ? '0.00' : amount.toFixed(2);
}

function generateRandonColour()
{
    var r = Math.floor(Math.random() * 255);
    var g = Math.floor(Math.random() * 255);
    var b = Math.floor(Math.random() * 255);

    return "rgb(" + r + "," + g + "," + b + ")";
}

function calculateChartData(tableElement, label, rowAttributeName = '[data-table-row]')
{
    var labels = [];
    var data = [];
    var colors = [];

    $(tableElement).find(rowAttributeName).each(function(index, element) {
        labels.push($(element).find('[data-table-label]').text().replace(/[\s\n]+/g, ''));
        data.push(sanitizeAmount($(element).find('[data-table-amount]').text()));
        colors.push(generateRandonColour());
    });   
    
    return {
        labels : labels,
        datasets : [{
            label : label,
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
        labels.push($(element).find('[data-table-label]').text().replace(/[\s\n]+/g, ''));
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