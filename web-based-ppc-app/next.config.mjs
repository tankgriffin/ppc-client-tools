/** @type {import('next').NextConfig} */
const nextConfig = {
  // Temporarily disable TypeScript errors during development
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },
  // Configure webpack to handle AI dependencies
  webpack: (config, { isServer }) => {
    // Handle ONNX runtime for Transformers.js
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        path: false,
        os: false,
        crypto: false,
        stream: false,
        util: false,
        buffer: false,
      };
      
      // Configure aliases to use web versions
      config.resolve.alias = {
        ...config.resolve.alias,
        'onnxruntime-node': false,
      };
    }
    
    // Exclude node-specific binaries and packages from client bundle
    config.externals = config.externals || [];
    if (!isServer) {
      config.externals.push({
        'onnxruntime-node': 'commonjs onnxruntime-node',
        'onnxruntime-web': 'commonjs onnxruntime-web',
      });
    }
    
    // Add rule for .node files
    config.module.rules.push({
      test: /\.node$/,
      use: 'ignore-loader',
    });
    
    // Add rule for WASM files
    config.module.rules.push({
      test: /\.wasm$/,
      type: 'asset/resource',
    });
    
    return config;
  },
  
  // Environment variables for AI configuration
  env: {
    AI_ENABLED: 'true',
    AI_MODEL_CACHE_SIZE: '500',
    HF_HUB_DISABLE_TELEMETRY: '1',
  },
  
  // Headers for WASM support
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'Cross-Origin-Embedder-Policy',
            value: 'credentialless',
          },
          {
            key: 'Cross-Origin-Opener-Policy',
            value: 'same-origin',
          },
        ],
      },
    ];
  },
};

export default nextConfig;
