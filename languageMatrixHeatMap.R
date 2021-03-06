require(gplots)
langlang <- read.csv('bindata.csv', header=TRUE)
langlang_matrix <- data.matrix(langlang)
rownames(langlang_matrix) <- colnames(langlang_matrix)
langlang_heatmap <- heatmap.2(langlang_matrix, Rowv=NA, Colv=NA, col=cm.colors(2),scale="column",trace="none",margins=c(5,10))
