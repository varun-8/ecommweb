import clientPromise from '@/lib/mongodb'
import { MongoDBAdapter } from '@auth/mongodb-adapter'
import NextAuth, { getServerSession } from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'


const adminEmails = ['varunsiva88@gmail.com','ecommercewebsite04@gmail.com']; // only this user can sign in to the admin page

  
  export const authOptions = {
    providers: [
      GoogleProvider({
        clientId: process.env.GOOGLE_ID,
        clientSecret: process.env.GOOGLE_SECRET,
      
      }),
    ],
    adapter: MongoDBAdapter(clientPromise),
    callbacks: {
      session: ({session,token,user}) => {
        if (adminEmails.includes(session?.user?.email)) {
          return session;
        } else {
          return false;
        }
      },
    },
  };
 
  export default NextAuth(authOptions);

  export async function isAdminRequest(req,res) {
    const session = await getServerSession(req,res,authOptions);
    if (!adminEmails.includes(session?.user?.email)) {
      res.status(401);
      res.end;
      throw 'not an admin';
    }
  }
  