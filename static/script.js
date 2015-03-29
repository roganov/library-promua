$(function () {
    'use strict';
    initAuthorsModal();
});
function initAuthorsModal() {
    'use strict';
    var authors = $('.js-authors'),
        modal = $('#modal'),
        modalAuthors = modal.find('.authors');
    if (authors.length === 0) {
        // checking that invoked on the right page
        return;
    }
    authors.on('click', '.author-remove', function () {
        var node = $(this).parent().parent();
        node.hide('slow', function () {
            node.remove();
            if (authors.children().length === 0) {
                authors.prev().show(); // show the 'no-authors' caption
            }
        });
    });
    modal.find('.js-select').click(function () {
        var id = modalAuthors.find('input:checked').val();
        insertAuthor(authors, id, modal.data('name'));
        modal.modal('hide');
    });
    modal.find('.js-new').click(function () {
        createInsertAuthor(authors, modal.data('name'));
        modal.modal('hide');
    });
    $('.js-add-author').click(function () {
        var input = $(this).parent().parent().find('input'),
            name = input.val();
        input.val('');
        if (name === '') {
            input.focus();
            return;
        }
        modal.data('name', name);
        $.ajax('/authors',
            {
                method: 'GET',
                data: {
                    'with_books': 1,
                    name: name
                },
                success: function (data) {
                    var result = data.result,
                        len = result.length;
                    if (len) {
                        modalAuthors.empty();
                        for (var i = 0; i < len; i++) {
                            var node = $(modalRadioTempl(result[i]));
                            modalAuthors.append(node);
                        }
                        modal.modal();
                    } else {
                        createInsertAuthor(authors, name);
                    }
                }
            }
        );
    });
}
function insertAuthor(authors, authorId, name) {
    'use strict';
    var lastInput = authors.find('input').last(),
        id;
    if (lastInput.length) {
        id = Number(lastInput.attr('name').split('-')[1]) + 1;
    } else {
        id = 0;
    }

    var nodes = $(authorTempl(id, authorId, name));
    authors.prev().hide();
    authors.append(nodes);
}
function createInsertAuthor(authors, name) {
    'use strict';
    $.ajax('/authors/add', {
        method: 'POST',
        data: {
            name: name,
            csrf_token: $("#csrf_token").val()
        },
        success: function (data) {
            insertAuthor(authors, data.id, data.name);
        }
    });
}
function authorTempl(i, id, name) {
    'use strict';
    return "<li>" +
        "<input type='hidden' name='author_ids-" + i + "' value='" + id + "'>" +
        escape(name) +
        "<a><span class='author-remove text-muted glyphicon glyphicon-remove-sign'></span></a>" +
        "</li>";
}
function modalRadioTempl(author) {
    return '<div class="radio">' +
        '<label>' +
        '<input type="radio" name="author_id" value="' + author.id + '" checked>' +
        escape(author.name) + '<br><span class="text-muted">Author of:</span> ' + escape(author.books.join(', ')) +
        '</label>' +
        '</div>';
}
function escape(html) {
    // hacky way to escape html
    return $('<div/>').text(html).html();
}