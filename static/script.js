$(function () {
    'use strict';
    initAuthorsModal();

    // highlighting
    var title = getParameterByName('title').trim(),
        author = getParameterByName('author').trim();
    if (location.pathname.match(/^\/authors/)) {
        // select second and third rows and highlight author and title query respectively
        $(".table td:nth-child(2)").find("a,li").addBack().highlight(author, 'highlight');
        $(".table td:nth-child(3)").find("a,li").addBack().highlight(title, 'highlight');
    } else if (location.pathname.match(/^\/books/)) {
        // on the books page authors and title cols are switched
        $(".table td:nth-child(2)").find("a,li").addBack().highlight(title, 'highlight');
        $(".table td:nth-child(3)").find("a,li").addBack().highlight(author, 'highlight');
    }
});
function initAuthorsModal() {
    'use strict';
    var authors = $('.js-authors'),
        authorInput = $('input[name="author"]'),
        modal = $('#modal'),
        modalAuthors = modal.find('.authors');
    if (authors.length === 0) {
        // checking that invoked on the right page
        return;
    }

    var addAuthor = function () {
        var  name = authorInput.val().trim();
        authorInput.val('');
        if (name === '') {
            authorInput.focus();
            return;
        }
        // change the submit button text to 'Loading...' while adding a new author
        $('.js-mainBtn').button('loading');
        modal.data('name', name);
        $.ajax('/api/authors', {
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
            },
            error: function (resp) {
                alert('Unexpected error: ' + resp.responseText);
            }
        });
    };

    modal.on('hidden.bs.modal', function(e) {
        $('.js-mainBtn').button('reset');
    });

    // handle button clicks on the modal
    modal.find('.js-select').click(function () {
        // user selected an existing author
        var id = modalAuthors.find('input:checked').val();
        insertAuthor(authors, id, modal.data('name'));
        modal.modal('hide');
    });
    modal.find('.js-new').click(function () {
        // user decided to create a new author with the same nama
        createInsertAuthor(authors, modal.data('name'));
        modal.modal('hide');
    });
    // remove author from the book when a user presses the remove sign
    authors.on('click', '.author-remove', function () {
        var node = $(this).parent().parent();
        node.hide('slow', function () {
            node.remove();
            if (authors.children().length === 0) {
                authors.prev().removeClass('hide'); // show the 'no-authors' caption
            }
        });
    });

    // listeners that add a new author
    $('.js-add-author').click(addAuthor);
    authorInput.keydown(function (e) {
        if (e.keyCode === 13) { // return key
            e.preventDefault();
            addAuthor();
        }
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
    authors.prev().addClass('hide');
    authors.append(nodes);
    $('.js-mainBtn').button('reset');
}
function createInsertAuthor(authors, name) {
    'use strict';
    $.ajax('/api/authors/add', {
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
        "<input type='hidden' name='authors-" + i + "' value='" + id + "'>" +
        escape(name) +
        "<a><span class='author-remove text-muted glyphicon glyphicon-remove-sign'></span></a>" +
        "</li>";
}
function modalRadioTempl(author) {
    'use strict';
    return '<div class="radio">' +
        '<label>' +
        '<input type="radio" name="author_id" value="' + author.id + '" checked>' +
        escape(author.name) + '<br><span class="text-muted">Author of:</span> ' + escape(author.books.join(', ')) +
        '</label>' +
        '</div>';
}
function escape(html) {
    // hacky way to escape html
    'use strict';
    return $('<div/>').text(html).html();
}
function getParameterByName(name) {
    // http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript/901144#901144
    'use strict';
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
    return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
jQuery.fn.highlight = function (str, className) {
    'use strict';
    var regex = new RegExp(str, "gi");
    return this.each(function () {
        $(this).contents().filter(function() {
            return this.nodeType === 3 && regex.test(this.nodeValue);
        }).replaceWith(function() {
            return (this.nodeValue || "").replace(regex, function(match) {
                return "<span class=\"" + className + "\">" + match + "</span>";
            });
        });
    });
};
