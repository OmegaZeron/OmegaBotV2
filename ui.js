$('#tabs').w2tabs({
    name: 'chatTabs',
    active: 'tab1',
    tabs: [
        { id: '#omegazeron', caption: 'OmegaZeron', closable: true },
        { id: '#alphabuttsoup', caption: 'AlphaButtSoup', closable: true }
    ],
    onClick: function (event) {
        changeSomething(event.target)
    }
});

let pstyle = 'background-color: #F5F6F7; border: 1px solid #dfdfdf; padding: 5px;';
$('#chat').w2layout({
    name: 'chatLayout',
    panels: [
        {type: 'top', size: 550, resizable: true, style: pstyle},
        {type: 'bottom', size: 50, resizable: true, style: pstyle}
    ]
})

function changeSomething(target)
{
    $('#chat').html(target);
}