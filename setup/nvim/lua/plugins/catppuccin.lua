return {
    "catppuccin/nvim",
    tag = "v1.10.0",
    name = "cappuccin",
    priority = 1000,
    config = function()
        vim.cmd.colorscheme "catppuccin"
    end
}
