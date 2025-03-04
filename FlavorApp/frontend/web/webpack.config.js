module.exports = {
  "performance": {
    "hints": {
      "maxAssetSize": 250000,
      "maxEntrypointSize": 250000
    },
    "optimization": {
      "splitChunks": {
        "chunks": "all",
        "minSize": 20000,
        "maxSize": 250000
      }
    }
  }
}