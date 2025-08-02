vim.g.mapleader = " "
vim.g.maplocalleader = "\\"

vim.opt.expandtab = true
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4
vim.opt.softtabstop = 4

vim.opt.number = true

vim.keymap.set({'n', 'v'}, '<C-c>', '"+y', { noremap = true, silent = true })

