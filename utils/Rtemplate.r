#!/bin/env Rscript
# coding: utf-8


#######################################################
# Method 1
args <- commandArgs()
file <- args[6]

# 第一个命令行输入的参数是args[6]，若想ars[1]表示第一个输入的参数，则使用commandArgs(trailling=TRUE)


#######################################################
# Method 2

library('optparse')

option_list <- list(
    make_option(c('--file', '-f'), type='character', default=NULL, help='dataset file.', metavar='file')
    make_option(c('--out', '-o'), type='character', default='out.txt', help='output file name', metavar='output')
    )

opt_parser <- OptionParser(option_list=option_list)
opt <- parse_args(opt_parser) 

file <- opt$file