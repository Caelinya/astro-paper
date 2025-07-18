import type { APIRoute } from "astro";
import { getCollection, type CollectionEntry } from "astro:content";
import { getPath } from "@/utils/getPath";
import { generateOgImageForPost } from "@/utils/generateOgImages";
import { SITE } from "@/config";

export async function getStaticPaths() {
  if (!SITE.dynamicOgImage) {
    return [];
  }

  const posts = await getCollection("posts").then(p =>
    p.filter(({ data }) => !data.draft && !data.ogImage)
  );

  return posts.map(post => ({
    params: { slug: post.slug },
    props: post,
  }));
}

export const GET: APIRoute = async ({ props }) => {
  if (!SITE.dynamicOgImage) {
    return new Response(null, {
      status: 404,
      statusText: "Not found",
    });
  }

  return new Response(
    await generateOgImageForPost(props as CollectionEntry<"posts">),
    {
      headers: { "Content-Type": "image/png" },
    }
  );
};
