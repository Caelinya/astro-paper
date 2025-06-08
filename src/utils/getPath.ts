/**
 * Get full path of a blog post
 * @param slug - slug of the blog post
 * @returns blog post path
 */
export function getPath(slug: string) {
  return `/posts/${slug}`;
}
