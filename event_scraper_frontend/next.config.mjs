/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://34.67.19.243:5000/api/:path*', // HTTP backend
      },
    ];
  },
};

export default nextConfig;

