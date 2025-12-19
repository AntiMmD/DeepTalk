import { Link } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

interface PostCardProps {
  id: string;
  author: string;
  title: string;
  excerpt: string;
}

const PostCard = ({ id, author, title, excerpt }: PostCardProps) => {
  return (
    <Card className="animate-fade-in border-0 border-b rounded-none last:border-b-0 shadow-none hover:shadow-none bg-card">
      <CardHeader className="pb-2">
        <span className="text-xs font-bold text-muted-foreground uppercase tracking-wide">
          {author}
        </span>
        <CardTitle className="mt-1">
          <Link
            to={`/post/${id}`}
            className="hover:text-primary transition-colors"
          >
            {title}
          </Link>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted-foreground leading-relaxed">
          {excerpt}
          <Link
            to={`/post/${id}`}
            className="ml-1 font-semibold text-foreground hover:text-primary transition-colors"
          >
            Read More...
          </Link>
        </p>
      </CardContent>
    </Card>
  );
};

export default PostCard;
